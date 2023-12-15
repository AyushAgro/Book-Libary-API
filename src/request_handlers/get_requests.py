from abc import ABC

from src.utils import (book_category_view, cart_table, category_table,
                       exceptions, methods, orders_table, users_table)

from .base_class import LibraryRequestHandler, log_and_notify


class GetAvailableBooksHandler(LibraryRequestHandler, ABC):

    async def get(self):
        log_and_notify.info(
            f'Fethching all avilable books with param {self.param}')
        category = self.param.get('category', None)
        title = self.param.get('title', None)
        author = self.param.get('author', None)
        filter_operation = self.param.get('filter_operation', 'AND')
        published_year = self.param.get('published_year', None)
        book_idx = self.param.get('book_idx', None)
        avilable_book_in_library_db_resp = await book_category_view.filter_category_author_title_publishes_year_or_return_all_avilable_books(
            category=category,
            title=title,
            author=author,
            published_year=published_year,
            book_idx=book_idx,
            filter_operation=filter_operation)
        self.return_result(avilable_book_in_library_db_resp)


class GetUserCartBooksHandler(LibraryRequestHandler, ABC):

    async def get(self):
        log_and_notify.info(
            f'Fetching all user books in cart with param {self.param}')

        user_idx = self.user_data.get_id()
        book_in_cart_for_user_db_resp = await cart_table.fetch_all_books_present_in_user_cart(
            user_idx=user_idx)
        self.return_result(book_in_cart_for_user_db_resp)


class GetPastUserOrdersHandler(LibraryRequestHandler, ABC):

    async def get(self):
        log_and_notify.info(
            f'Fetching user all past orders with param {self.param}')
        user_idx = self.user_data.get_id()
        past_order_db_resp = await orders_table.fetch_formatted_user_past_order_using_book_catgory_view(
            user_idx=user_idx)
        self.return_result(past_order_db_resp)


class GetAllUserOrdersHandler(LibraryRequestHandler, ABC):

    async def get(self):
        log_and_notify.info(
            f'Fetching all user past orders with param {self.param}')
        past_order_db_resp = await orders_table.fetch_formatted_user_past_order_using_book_catgory_view(
        )
        self.return_result(past_order_db_resp)


class GetAvailableCategoryHandler(LibraryRequestHandler, ABC):

    async def get(self):
        log_and_notify.info(
            f'Fetching all available category with param {self.param}')
        category_db_resp = await category_table.fetch_all_avilable_category()
        self.return_result(category_db_resp)


# Expires=Fri, 16 Jun 2023 23:38:16 GMT;
# User Login
class LoginUserHandler(LibraryRequestHandler, ABC):

    async def get(self):
        email_address = self.param.get('email')
        password = self.param.get('password')
        password_hashed = methods.hash_user_password_using_Sha512(password)

        is_email_present = await users_table.is_email_present(
            email=email_address)
        if not is_email_present:
            raise exceptions.UnknownUserException(email_address=email_address)
        is_user_present = await users_table.validate_user_email_and_password(
            email_address, password_hashed)
        self.set_secure_cookie('email', email_address, expires_days=3)
        if is_user_present:
            msg = f'Welcome {email_address}, You are successfully logged in'
        else:
            msg = 'Incorrect email or password, please check your credentials'
        output = {'msg': msg}
        self.return_result(output)
