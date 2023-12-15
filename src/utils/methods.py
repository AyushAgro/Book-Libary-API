import codecs
import datetime
import hashlib
import io
import json
import random
from decimal import Decimal

from src.utils.data_class import (Cart, DataClass, date_default_format,
                                  datetime_default_format)


class JsonBaseEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """

    def default(self, obj):
        if isinstance(obj, io.StringIO) or isinstance(obj, io.BytesIO):
            return codecs.decode(obj.getvalue(), encoding="ISO-8859-1")
        elif isinstance(obj, datetime.datetime):
            return obj.strftime(datetime_default_format)
        elif isinstance(obj, datetime.date):
            return obj.strftime(date_default_format)
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, DataClass):
            return obj.to_json()
        return json.JSONEncoder.default(self, obj)


def hash_user_password_using_Sha512(password):
    return hashlib.sha512(password.encode()).hexdigest()


def format_cart_resp_to_order_input(db_resp):
    total_amount = 0
    quantity = {}
    books_idx_dict = {}
    if isinstance(db_resp, dict):
        header = db_resp.get('header')
        values = db_resp.get('values')
        for single_book_value in values:
            book_price = single_book_value[header.index('price')]
            book_idx = single_book_value[header.index('book_idx')]
            if isinstance(book_price, Decimal):
                book_price = float(book_price)
            quantity[book_idx] = quantity.get(book_idx, 0) + 1
            books_idx_dict[book_idx] = f'{quantity[book_idx]}^{book_price}'
            total_amount += book_price
    else:
        books_detail = db_resp
        for single_book_details in books_detail:
            if isinstance(single_book_details, Cart):
                book_idx = single_book_details.book_idx
                book_price = single_book_details.price
                quantity[book_idx] = quantity.get(book_idx, 0) + 1
                books_idx_dict[book_idx] = f'{quantity[book_idx]}^{book_price}'
                total_amount += book_price
    return {'books_idx_dict': books_idx_dict, 'total_amount': total_amount}


def format_time(start_time, end_time):
    total_runtime = end_time - start_time
    if total_runtime > 60:
        total_runtime = f'{int(total_runtime // 60)} Minutes and {int(total_runtime % 60)} Seconds'
    elif int(total_runtime) != 0:
        total_runtime = f'{int(total_runtime)} Seconds'
    else:
        total_runtime = f'{int(total_runtime * 1000)} MiliSeconds'
    return total_runtime


def uniqueid():
    seed = random.getrandbits(32)
    while True:
        yield seed
        seed += 1
