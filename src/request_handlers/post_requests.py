import datetime
from abc import ABC

from src.config import config, log_and_notify
from src.utils import (books_table, cart_table, category_table, exceptions,
                       methods, orders_table, users_table)

from .base_class import LibraryRequestHandler

threshold_time_to_remove_book_in_minute = 30


class LogoutUserHandler(LibraryRequestHandler, ABC):

    def post(self):
        self.clear_all_cookies()
        # self.redirect('/')


# User Register
class RegisterUserHandler(LibraryRequestHandler, ABC):

    async def post(self):
        email_address = self.param.get('email')
        password = self.param.get('password')
        password_hashed = methods.hash_user_password_using_Sha512(password)
        is_email_present = await users_table.is_email_present(
            email=email_address)
        if is_email_present:
            raise exceptions.EmailAlreadyExists(email_address)
        await users_table.insert_new_user(name=self.param.get('name', 'None'),
                                          email=email_address,
                                          password_hashed=password_hashed,
                                          is_admin=False,
                                          tags=self.param.get('tags', {}))
        output = {
            'msg':
            'Successfully inserted user, please login with your credential.'
        }
        self.return_result(output)


class AddBookToUserCartHandler(LibraryRequestHandler, ABC):

    async def post(self):
        user_idx = self.user_data.get_id()
        book_id = self.param.get('book_id')
        is_book_present_in_db = await books_table.is_book_present(
            book_id=book_id)
        # This can also be handle in db layer but handled here for better error message handling
        if not is_book_present_in_db:
            raise exceptions.BookNotFoundException(book_id=book_id)
        book_price = await books_table.get_book_amount(book_id)
        added_time = datetime.datetime.now()
        removal_time = added_time + datetime.timedelta(
            minutes=threshold_time_to_remove_book_in_minute)
        await cart_table.add_new_books_to_user_cart(user_idx=user_idx,
                                                    book_idx=book_id,
                                                    price=book_price,
                                                    added_time=added_time,
                                                    removal_time=removal_time)
        # Decreasing stock unit for the book id
        await books_table.decrease_stock_unit(book_id=book_id)

        output = {'msg': f'Successfully inserted book into your cart'}
        self.return_result(output)


# Order Checkout
class CheckoutUserOrderHandler(LibraryRequestHandler, ABC):

    async def post(self):
        user_idx = self.user_data.get_id()
        user_cart_db_resp = await cart_table.fetch_all_books_present_in_user_cart(
            user_idx=user_idx)
        cart_formaated_resp = methods.format_cart_resp_to_order_input(
            user_cart_db_resp)
        total_amount = cart_formaated_resp.get('total_amount')
        if total_amount == 0:
            output = {'msg': 'No item is present in cart for checkout.'}
        else:
            await orders_table.add_new_user_order(
                user_idx=user_idx,
                books_idx=cart_formaated_resp.get('books_idx_dict'),
                amount=total_amount)

            # deleting from cart only if order is placed sucesfully
            await cart_table.delete_all_books_present_in_user_cart(
                user_idx=user_idx)
            output = {
                'msg':
                f'Succesfully placed order, your total amount is {total_amount}'
            }
        self.return_result(output)


# Category Create
class InsertNewCategoryHandler(LibraryRequestHandler, ABC):

    async def post(self):
        user_idx = self.user_data.get_id()
        category_name = self.param.get('category')
        is_category_present_db_resp = await category_table.is_category_present(
            category_name=category_name)
        if is_category_present_db_resp:
            raise exceptions.CategoryNameNotFoundException(category_name)
        await category_table.insert_new_category(name=category_name,
                                                 added_user_idx=user_idx)
        msg = {'msg': f'Successfully inserted category {category_name}'}
        self.return_result(msg)


# Book Create
class InsertNewBookHandler(LibraryRequestHandler, ABC):

    async def post(self):
        user_idx = self.user_data.get_id()
        title = self.param.get('title')
        author = self.param.get('author')
        category_idx = self.param.get('category_idx')
        is_category_present_in_table = await category_table.is_category_present(
            category_idx=category_idx)
        if not is_category_present_in_table:
            raise exceptions.CategoryIndexNotFound(category_idx)
        published_year = self.param.get('published_year')
        price = self.param.get('price')
        stock_unit = self.param.get('stock_unit')
        tags = self.param.get('tags', {})
        await books_table.insert_book_details(title=title,
                                              author=author,
                                              category_idx=category_idx,
                                              published_year=published_year,
                                              price=price,
                                              stock_unit=stock_unit,
                                              tags=tags,
                                              added_user_idx=user_idx)
        output = {'msg': 'Successfully inserted book into library'}
        self.return_result(output)
