import datetime

from .base_class import DatabaseBaseClass, log_and_notify


class CartTable(DatabaseBaseClass):

    async def add_new_books_to_user_cart(self, user_idx, book_idx, price,
                                         added_time, removal_time) -> None:
        if isinstance(removal_time, datetime.datetime):
            removal_time = removal_time.strftime('%d-%m-%Y %H:%M:%S')
        if isinstance(added_time, datetime.datetime):
            added_time = added_time.strftime('%d-%m-%Y %H:%M:%S')
        log_and_notify.info(
            f'Inserting new book to cart for user {user_idx} and book_idx {book_idx}'
        )
        query = "INSERT INTO {table_name} (user_idx, book_idx, price, added_time, removal_time) values (%(user_idx)s, %(book_idx)s, %(price)s, to_timestamp(%(added_time)s, 'dd-mm-yyyy hh24:mi:ss'), to_timestamp(%(removal_time)s, 'dd-mm-yyyy hh24:mi:ss'))".format(
            table_name=self.table_name)
        query_param = {
            'user_idx': user_idx,
            'book_idx': book_idx,
            'price': price,
            'added_time': added_time,
            'removal_time': removal_time
        }
        self.execute_write_query(query=query, query_param=query_param)

    async def fetch_all_books_present_in_user_cart(self, user_idx):
        log_and_notify.info(f'Fetching all book in cart for user {user_idx}')
        query = 'select * from {table_name} where user_idx = %(user_idx)s and expired = false'.format(
            table_name=self.table_name)
        query_param = {'user_idx': user_idx}
        db_resp = self.execute_read_query(query=query, query_param=query_param)
        formatted_db_resp = await self.format_db_resp(db_resp)
        return formatted_db_resp

    async def delete_single_book_from_user_cart(self, user_idx,
                                                book_idx) -> None:
        log_and_notify.info(
            f'Deleting single books form chart for user {user_idx} and book {book_idx}'
        )
        query = """BEGIN;
                    LOCK TABLE {table_name} IN ROW EXCLUSIVE MODE;
                    SELECT * FROM {table_name} WHERE user_idx = %(user_idx)s and book_idx = %(book_idx)s FOR UPDATE;
                    
                    DELETE FROM {table_name} WHERE user_idx = %(user_idx)s and book_idx = %(book_idx)s;
                    
                    END;
        """.format(table_name=self.table_name)
        query_param = {'user_idx': user_idx, 'book_idx': book_idx}
        self.execute_write_query(query=query, query_param=query_param)

    async def delete_all_books_present_in_user_cart(self, user_idx) -> None:
        log_and_notify.info(
            f'Deleting all books form chart for user {user_idx}')
        # The EXCLUSIVE keyword locks a table in exclusive mode. This mode denies other
        # processes both read and write access to the table [ Both read and write will be stop]
        query = """BEGIN;
                    LOCK TABLE {table_name} IN ROW EXCLUSIVE MODE;
                    SELECT * FROM {table_name} WHERE user_idx = %(user_idx)s FOR UPDATE;
                    UPDATE books set stock_unit = stock_unit + 1 where id IN (select book_idx from {table_name} where user_idx = %(user_idx)s);
                    DELETE FROM  {table_name} WHERE user_idx = %(user_idx)s;
                    
                    END;
        """.format(table_name=self.table_name)

        query_param = {'user_idx': user_idx}
        self.execute_write_query(query=query, query_param=query_param)

    async def fetch_and_delete_user_cart(self, user_idx):
        db_resp = await self.fetch_all_books_present_in_user_cart(
            user_idx=user_idx)
        await self.delete_all_books_present_in_user_cart(user_idx=user_idx)
        formatted_db_resp = await self.format_db_resp(db_resp)
        return formatted_db_resp

    async def delete_expire_book_and_update_stock_unit_in_book_table(self):
        query = """BEGIN;
        LOCK TABLE {table_name} IN ROW EXCLUSIVE MODE;
        Select * from {table_name} where removal_time <= now() FOR UPDATE;
        UPDATE {table_name} set expired = true where removal_time < now();
        
        SELECT * FROM books where id IN (select book_idx from {table_name} where expired = true) FOR UPDATE;
        UPDATE books set stock_unit = stock_unit + 1 where id IN (select book_idx from {table_name} where expired = true);
        DELETE from {table_name} where expired = true;
        
        END;
        """.format(table_name=self.table_name)
        query_param = {}
        self.execute_write_query(query=query, query_param=query_param)

    async def delete_book_from_all_user_cart(self, book_idx):
        query = """BEGIN;
                    LOCK TABLE {table_name} IN ROW EXCLUSIVE MODE;
                    SELECT * FROM {table_name} WHERE book_idx = %(book_idx)s FOR UPDATE;
                    
                    DELETE FROM {table_name} where book_idx = %(book_idx)s;
                    
                    END;
        """.format(table_name=self.table_name)
        query_param = {'book_idx': book_idx}
        self.execute_write_query(query, query_param, verbose=True)

    async def delete_book_from_cart_and_book_table(self, book_idx):
        query = """BEGIN;
                    LOCK TABLE {table_name} IN ROW EXCLUSIVE MODE;
                    LOCK TABLE books IN ROW EXCLUSIVE MODE;
                    SELECT * FROM {table_name} WHERE book_idx = %(book_idx)s FOR UPDATE;
                    SELECT * FROM books WHERE id = %(book_idx)s FOR UPDATE;
                    
                    DELETE FROM {table_name} where book_idx = %(book_idx)s;
                    UPDATE books SET stock_unit = -1 where id =%(book_idx)s;
                    END;
        """.format(table_name=self.table_name)
        query_param = {'book_idx': book_idx}
        self.execute_write_query(query, query_param, verbose=True)

    async def delete_category_books_and_books_from_cart(self, category_idx):
        query = """BEGIN;
                    LOCK TABLE {table_name} IN ROW EXCLUSIVE MODE;
                    LOCK TABLE books IN ROW EXCLUSIVE MODE;
                    LOCK TABLE category IN ROW EXCLUSIVE MODE;
                    SELECT * from category where id = %(category_idx)s FOR UPDATE;
                    SELECT * FROM books WHERE category_idx = %(category_idx)s FOR UPDATE;
                    SELECT * FROM {table_name} WHERE book_idx in (SELECT id FROM books WHERE category_idx = %(category_idx)s) FOR UPDATE;
                        
                    UPDATE category set active = false where id = %(category_idx)s;
                    UPDATE books set stock_unit = -1 where category_idx = %(category_idx)s;
                    DELETE FROM {table_name} where book_idx in (select id from books where stock_unit <=0);
                    END;
        """.format(table_name=self.table_name)
        query_param = {'category_idx': category_idx}
        self.execute_write_query(query, query_param, verbose=True)
