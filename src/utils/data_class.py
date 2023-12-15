import datetime
from decimal import Decimal

default_int_value = 0000
default_str_value = 'None'

datetime_default_format = '%d/%m/%Y, %H:%M:%s'
date_default_format = '%d/%m/%Y'


class DataClass:

    def __init__(self, header=None, values=None):
        if values is None:
            values = []
        if header is None:
            header = []
        self.header = header
        self.values = values
        self.key_to_ignore = ['last_modified_at', 'created_at']
        self.rename_keys_mapping = {}
        self.id = None
        self.db_keys_to_return = []

    def set_params(self):
        self.db_keys_to_return = []
        for key, value in zip(self.header, self.values):
            if key not in self.key_to_ignore:
                # Common db conversion to python
                if isinstance(value, Decimal):
                    value = float(value)
                elif isinstance(value, datetime.datetime):
                    value = value.strftime(datetime_default_format)
                elif isinstance(value, datetime.date):
                    value = value.strftime(date_default_format)
                if key in self.rename_keys_mapping:
                    key = self.rename_keys_mapping[key]
                self.db_keys_to_return.append(key)
                setattr(self, key, value)

    def to_json(self):
        output = {
            key: value
            for key, value in self.__dict__.items()
            if key in self.db_keys_to_return
        }
        return output


class Book(DataClass):

    def __init__(self, header=None, values=None):
        super().__init__(header, values)
        self.title = default_str_value
        self.author = default_str_value
        self.category = default_str_value
        self.published_year = default_int_value
        self.price = default_int_value
        self.stock_unit = default_int_value
        self.tags = default_str_value
        self.added_user_id = default_int_value
        self.set_params()

    def is_book_avilable(self) -> bool:
        return self.stock_unit > 0

    def get_category(self) -> str:
        return self.category

    def get_author(self) -> str:
        return self.author

    def get_title(self) -> str:
        return self.title

    def get_price(self) -> float:
        return self.price


class User(DataClass):

    def __init__(self, header=None, values=None):
        super().__init__(header, values)
        self.id = default_int_value
        self.name = default_str_value
        self.email = default_str_value
        self.password = default_str_value
        self.is_admin = False
        self.tags = default_str_value
        self.last_login_timestamp = datetime.datetime
        self.user_logged_in = False
        self.set_params()

    def is_user_admin(self) -> bool:
        return self.is_admin

    def get_email(self) -> str:
        return self.email

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> int:
        return self.id

    def is_user_logged_in(self) -> bool:
        return self.user_logged_in

    def mark_user_logged_in(self):
        self.user_logged_in = True


class Cart(DataClass):

    def __init__(self, header=None, values=None):
        super().__init__(header, values)
        self.user_idx = default_int_value
        self.book_idx = default_int_value
        self.price = default_int_value
        self.added_time = datetime.datetime
        self.removal_time = datetime.datetime.now()
        self.set_params()

    # FUTURE:- rename function
    def is_book_cart_expire(self) -> bool:
        return self.removal_time < datetime.datetime.now()

    def get_book_idx(self) -> int:
        return self.book_idx

    def get_added_time(self):
        return self.added_time


class Order(DataClass):

    def __init__(self, header=None, values=None):
        super().__init__(header, values)
        self.book_idx = default_int_value
        self.user_idx = default_int_value
        self.title = default_str_value
        self.author = default_str_value,
        self.category_name = default_str_value
        self.published_year = default_int_value,
        self.current_stock_unit = default_int_value
        self.purchase_amount = default_int_value
        self.set_params()

    def get_books_idx(self) -> int:
        return self.book_idx

    def get_purchase_amount(self) -> float:
        return self.purchase_amount


class Category(DataClass):

    def __init__(self, header=None, values=None):
        super().__init__(header, values)
        self.name = default_str_value
        self.added_user_idx = default_int_value
        self.key_to_ignore.append('active')

        self.set_params()

    def get_name(self):
        return self.name


class BookCategory(Book):
    pass
