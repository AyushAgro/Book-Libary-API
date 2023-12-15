from abc import ABC

from src.utils import books_table, cart_table, category_table
from src.utils.exceptions import CategoryIndexNotFound

from .base_class import LibraryRequestHandler


# Cateogry Delete
class DeleteCategoryHandler(LibraryRequestHandler, ABC):

    async def delete(self):
        category_idx = self.param.get('category_idx')
        is_category_present_in_db = await category_table.is_category_present(
            category_idx=category_idx)
        if not is_category_present_in_db:
            raise CategoryIndexNotFound(category_idx)
        await cart_table.delete_category_books_and_books_from_cart(
            category_idx=category_idx)
        output = {
            f'Succesfully deleted category with index {category_idx} from library'
        }
        self.return_result(output)


# Book Delete
class DeleteSingleBookHandler(LibraryRequestHandler, ABC):

    async def delete(self):
        book_id = self.param.get('book_id')
        await books_table.delete_book_details(book_id=book_id)
        await cart_table.delete_book_from_cart_and_book_table(book_idx=book_id)
        output = {'msg': 'Successfully deleted book'}
        self.return_result(output)


# Empty Cart
class EmptyUserCart(LibraryRequestHandler, ABC):

    async def delete(self):
        user_idx = self.user_data.get_id()
        await cart_table.delete_all_books_present_in_user_cart(
            user_idx=user_idx)
        output = {'msg': 'Succesfully deleted all books from the cart'}
        self.return_result(output)
