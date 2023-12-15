from src.utils import exceptions

from .base_class import DatabaseBaseClass, log_and_notify


class BooksTable(DatabaseBaseClass):

    async def update_book_details(self, book_id, *args, **kwargs) -> None:
        query_param = {'book_id': book_id}
        update_query = ''
        book_table_columns = [
            'title', 'price', 'author', 'published_year', 'category_idx'
        ]
        for key, value in kwargs.items():
            if key in book_table_columns and value is not None:
                query_param[key] = value
                update_query += f' {key} = %({key})s,'
        if update_query == '':
            raise exceptions.DatabaseException(
                f'Please pass any one of the following param to update book details {book_table_columns}'
            )
        if update_query.endswith(','):
            update_query = update_query[:-1]

        query = 'UPDATE {table_name} set {update_query} where id = %(book_id)s'.format(
            table_name=self.table_name, update_query=update_query)
        self.execute_write_query(query, query_param)

    async def delete_book_details(self, book_id) -> None:
        log_and_notify.info(f'Deleting book with id {book_id}')
        query = 'Update {table_name} set stock_unit = -1 where id = %(book_id)s'.format(
            table_name=self.table_name)
        query_param = {'book_id': book_id}
        self.execute_write_query(query=query, query_param=query_param)

    async def insert_book_details(self, title, author, category_idx,
                                  published_year, stock_unit, tags, price,
                                  added_user_idx) -> None:
        log_and_notify.info(
            f'Inserting New book with title {title} and author {author}')
        query = 'INSERT INTO {table_name} (title, author, category_idx, published_year, stock_unit, tags, added_user_idx, price) VALUES (%(title)s, %(author)s, ' \
                '%(category_idx)s, %(published_year)s, %(stock_unit)s, %(tags)s, %(added_user_idx)s, %(price)s)'.format(
            table_name=self.table_name)
        query_param = {
            'title': title,
            'author': author,
            "category_idx": category_idx,
            "published_year": published_year,
            "stock_unit": stock_unit,
            "tags": self.process_tags_columns(tags),
            'price': price,
            "added_user_idx": added_user_idx
        }
        self.execute_write_query(query=query, query_param=query_param)
        log_and_notify.info(
            f'Inserted New book with title {title} and author {author}')

    async def is_book_present(self, book_id) -> bool:
        log_and_notify.info(f"Checking if book is present with id {book_id}")
        query = 'select * from {table_name} where id = %(book_id)s and stock_unit > 0'.format(
            table_name=self.table_name)
        query_param = {'book_id': book_id}
        db_resp = self.execute_read_query(query=query, query_param=query_param)
        values = db_resp.get('values')
        if len(values) > 0 and len(values[0]) > 0: return True
        return False

    async def get_book_amount(self, book_id) -> float:
        log_and_notify.info(f"Checking if book is present with id {book_id}")
        query = 'select price from {table_name} where id = %(book_id)s'.format(
            table_name=self.table_name)
        query_param = {'book_id': book_id}
        db_resp = self.execute_read_query(query=query, query_param=query_param)
        values = db_resp.get('values')
        return values[0][0]

    async def decrease_stock_unit(self, book_id):
        query = 'UPDATE {table_name} set stock_unit = stock_unit -1 where id = %(book_id)s'.format(
            table_name=self.table_name)
        query_param = {'book_id': book_id}
        self.execute_write_query(query=query, query_param=query_param)
