import datetime
import functools

from tornado import ioloop
from tornado.web import Application

from src.config import config, env_run, log_and_notify
from src.request_handlers import delete_requests as delete_req
from src.request_handlers import get_requests as get_req
from src.request_handlers import patch_requests as patch_req
from src.request_handlers import post_requests as post_req
from src.utils import cart_table

cart_removal_iolopp_timeout = 10


async def check_and_removal_expired_book_from_cart_recurisve_call():
    # log_and_notify.info('Removing all expired books from cart')
    await cart_table.delete_expire_book_and_update_stock_unit_in_book_table()
    # Re-hit the function after 10 second
    ioloop_instance.add_timeout(
        datetime.timedelta(seconds=cart_removal_iolopp_timeout),
        functools.partial(
            check_and_removal_expired_book_from_cart_recurisve_call))


"""
Edge Case
1. If the category is deleted [ the book in book_table should be deleted and also from cart the book should be deleted] Use cascade
2. If book is deleted [ book on cart should be deleted] Use cascade
3. If book is removed from cart , the book in stock should be inserted [ This has be be single transcation]
4. If order is placed successfully then only cart should be deleted.
5. For fetching available book, regex, exact string both should be applied, also both and and or operation should be applied [cautionary doc]
6. CUD permission on category and book should be admin 
7. Before adding book to cart check stock unit 
8. If the book is deleted , the book id is not deleted from past order, so we should keep minimum information in past order table [ such as price, category, title, published_price]. 
"""

cokkie_secret_key = config['CokkieSecretKey']


def make_app() -> Application:
    url_prefix = config['Gateway_api']['url_prefix']
    urls = [
        # User Auth
        ('/login', get_req.LoginUserHandler),
        ('/logout', post_req.LogoutUserHandler),
        ('/register', post_req.RegisterUserHandler),
        # Cart
        ('/add_to_cart', post_req.AddBookToUserCartHandler),
        ('/list_books_in_cart', get_req.GetUserCartBooksHandler),
        ('/empty_cart', delete_req.EmptyUserCart),
        # Order
        ('/checkout_order', post_req.CheckoutUserOrderHandler),
        ('/fetch_user_past_orders', get_req.GetPastUserOrdersHandler),
        # Fetch User Past Orders
        ('/fetch_all_past_orders', get_req.GetAllUserOrdersHandler),

        # Category
        ('/create_category', post_req.InsertNewCategoryHandler),
        ('/fetch_category', get_req.GetAvailableCategoryHandler),
        ('/update_category', patch_req.UpdateCategoryNameHandler),
        ('/delete_category', delete_req.DeleteCategoryHandler),
        # Books
        ('/add_book', post_req.InsertNewBookHandler),
        ('/fetch_books', get_req.GetAvailableBooksHandler),
        ('/update_book_details', patch_req.UpdateBookDetailsHandler),
        ('/delete_book', delete_req.DeleteSingleBookHandler)
    ]
    urls = [(url_prefix + url, handler) for url, handler in urls]
    tornado_application = Application(urls,
                                      debug=config['Gateway_api']['debug'],
                                      cookie_secret=cokkie_secret_key)
    return tornado_application


if __name__ == '__main__':
    ioloop_instance = ioloop.IOLoop().current()
    log_and_notify.critical(
        f"Starting Library API {env_run.capitalize()} Service !!")
    app = make_app()
    app.listen(config['Gateway_api']['port'])
    ioloop_instance.add_timeout(
        datetime.timedelta(seconds=0),
        functools.partial(
            check_and_removal_expired_book_from_cart_recurisve_call))

    ioloop_instance.start()
