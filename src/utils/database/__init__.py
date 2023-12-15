from .users import UsersTable
from .cart import CartTable
from .orders import OrdersTable
from .book_category_view import BookCategoryView
from .books import BooksTable
from .category import CategoryTable
import src.utils.data_class as dc

books_table = BooksTable(db_name='LibraryDatabase', table_name='books', data_class=dc.Book)
cart_table = CartTable(db_name='LibraryDatabase', table_name='cart', data_class=dc.Cart)
orders_table = OrdersTable(db_name='LibraryDatabase', table_name='orders', data_class=dc.Order)
users_table = UsersTable(db_name='LibraryDatabase', table_name='users', data_class=dc.User)
category_table = CategoryTable(db_name='LibraryDatabase', table_name='category', data_class=dc.Category)
book_category_view = BookCategoryView(db_name='LibraryDatabase', table_name='book_category_view', data_class= dc.BookCategory)
