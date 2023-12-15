from .base_class import DatabaseBaseClass, log_and_notify


class OrdersTable(DatabaseBaseClass):

    async def add_new_user_order(self, user_idx, books_idx, amount, *args,
                                 **kwargs) -> None:
        log_and_notify.info(
            f'Adding new order for user {user_idx} with amount {amount}')
        query = 'INSERT INTO {table_name} (user_idx, books_idx, amount) VALUES (%(user_idx)s, %(books_idx)s, %(amount)s)'.format(
            table_name=self.table_name)
        if isinstance(books_idx, dict):
            books_idx = self.process_tags_columns(books_idx)
        query_param = {
            'user_idx': user_idx,
            'books_idx': books_idx,
            'amount': amount
        }
        self.execute_write_query(query=query, query_param=query_param)
        log_and_notify.info(f'Added order for user {user_idx}')

    async def fetch_past_user_order(self, user_idx, *args, **kwargs) -> dict:
        log_and_notify.info(f'Fetching past order history for user {user_idx}')
        query = 'SELECT * FROM {table_name} where user_idx = %(user_idx)s'.format(
            table_name=self.table_name)
        query_param = {'user_idx': user_idx}
        db_resp = self.execute_read_query(query=query, query_param=query_param)
        return db_resp

    async def fetch_formatted_user_past_order_using_book_catgory_view(
            self, user_idx=None, *args, **kwargs):
        # Fixme:- Optimize the query and rename the table name
        if user_idx is not None:
            query = """select book_category_view.book_idx,
           book_category_view.title,
           book_category_view.author,
           book_category_view.category_name,
           book_category_view.published_year,
           order_unnest.quantity         as purchase_quantity,
           order_unnest.price            as    purchase_amount,
           order_unnest.quantity * order_unnest.price as total_amount

            from book_category_view
             join (select (string_to_array(n.book_tags, ':'))[1]::int     as id,
                          (string_to_array((string_to_array(n.book_tags, ':'))[2], '^'))[1]::int as quantity,
                          (string_to_array((string_to_array(n.book_tags, ':'))[2], '^'))[2]::decimal as price,
                          n.user_idx
                   from (select unnest(string_to_array(books_idx, '<>')) as book_tags, user_idx
                         from {table_name}
                         where user_idx = %(user_idx)s) as n
                   where n.book_tags != '') as order_unnest
                  on book_idx = order_unnest.id;
            """.format(table_name=self.table_name)
            query_param = {'user_idx': user_idx}
        else:
            query = """select book_category_view.book_idx,
            book_category_view.title,
            book_category_view.author,
            book_category_view.category_name,
            book_category_view.published_year,
           order_unnest.quantity         as purchase_quantity,
           order_unnest.price            as    purchase_amount,
           order_unnest.quantity * order_unnest.price as total_amount
             from book_category_view
              join (select (string_to_array(n.book_tags, ':'))[1]::int     as id,
                          (string_to_array((string_to_array(n.book_tags, ':'))[2], '^'))[1]::int as quantity,
                          (string_to_array((string_to_array(n.book_tags, ':'))[2], '^'))[2]::decimal as price,
                           n.user_idx
                    from (select unnest(string_to_array(books_idx, '<>')) as book_tags, user_idx
                          from {table_name}
                          ) as n
                    where n.book_tags != '') as order_unnest
                   on book_idx = order_unnest.id;
             """.format(table_name=self.table_name)
            query_param = {}
        db_resp = self.execute_read_query(query=query, query_param=query_param)
        formatted_db_resp = await self.format_db_resp(db_resp)
        return formatted_db_resp
