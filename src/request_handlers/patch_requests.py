from abc import ABC

from src.utils import books_table, category_table, exceptions

from .base_class import LibraryRequestHandler, log_and_notify


class UpdateCategoryNameHandler(LibraryRequestHandler, ABC):

    async def patch(self):
        old_category = self.param.get('old_category')
        new_category = self.param.get('new_category')
        is_old_category_present_db_resp = await category_table.is_category_present(
            category_name=old_category)
        if not is_old_category_present_db_resp:
            raise exceptions.CategoryNameNotFoundException(old_category)

        is_new_category_present_db_resp = await category_table.is_category_present(
            category_name=new_category)
        if is_new_category_present_db_resp:
            raise exceptions.LibraryAPIBaseException(
                f'Category with name {new_category} already present, please pass different name'
            )
        await category_table.update_category(old_category_name=old_category,
                                             new_category_name=new_category)
        output = {'msg': 'Successfully updated category name'}
        self.return_result(output)


class UpdateBookDetailsHandler(LibraryRequestHandler, ABC):

    async def patch(self):
        book_id = self.param.get('book_id')
        is_book_present_db_resp = await books_table.is_book_present(book_id)
        if not is_book_present_db_resp:
            raise exceptions.BookNotFoundException(book_id)
        title = self.param.get('title')
        author = self.param.get('author')
        category_idx = self.param.get('category_idx')
        published_year = self.param.get('published_year')
        price = self.param.get('price')

        await books_table.update_book_details(
            book_id=book_id,
            title=title,
            author=author,
            category_idx=category_idx,
            published_year=published_year,
            price=price,
        )
        output = {'msg': 'Successfully update books details'}
        self.return_result(output)
