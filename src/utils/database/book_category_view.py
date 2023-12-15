from .base_class import DatabaseBaseClass, database_delimiter, log_and_notify


class BookCategoryView(DatabaseBaseClass):

    async def filter_category_author_title_publishes_year_or_return_all_avilable_books(
            self, *args, **kwargs):
        filter_operation = kwargs.get('filter_operation').upper()
        log_and_notify.info(
            f'Fetching all avilable books with kwargs {kwargs}')
        query = f'SELECT * FROM {self.table_name} where stock_unit > 0 '
        query_param = {}
        where_query = ''
        where_clause = False
        if "category" in kwargs and kwargs.get('category') is not None:
            kwargs['category'] = str(
                kwargs['category']).split(database_delimiter)
            if where_clause:
                where_query += f' {filter_operation} '
            category_array = []
            for single_category in kwargs['category']:
                single_category = single_category.lower().strip()
                if single_category != '':
                    category_array.append('%' + single_category + '%')
            where_query += ' Lower(category_name) ILIKE ANY(%(category_array)s) '
            query_param['category_array'] = category_array
            where_clause = True
        if "title" in kwargs and kwargs.get('title') is not None:
            kwargs['title'] = str(kwargs['title']).split(database_delimiter)
            if where_clause:
                where_query += f' {filter_operation} '
            title_array = []
            for single_title in kwargs['title']:
                single_title = single_title.lower().strip()
                if single_title != '':
                    title_array.append('%' + single_title + '%')
            where_query += ' LOWER(title) ILIKE ANY(%(title_array)s) '
            query_param['title_array'] = title_array
            where_clause = True
        if "author" in kwargs and kwargs.get('author') is not None:
            kwargs['author'] = str(kwargs['author']).split(database_delimiter)
            if where_clause:
                where_query += f' {filter_operation} '
            author_array = []
            for single_author in kwargs['author']:
                single_author = single_author.lower().strip()
                if single_author != '':
                    author_array.append('%' + single_author + '%')
            where_query += f' LOWER(author) ILIKE ANY(%(author_array)s) '
            query_param['author_array'] = author_array
            where_clause = True
        if 'published_year' in kwargs and kwargs.get(
                'published_year') is not None:
            if where_clause:
                where_query += f' {filter_operation} '
            where_query += f' published_year = %(published_year)s '
            query_param['published_year'] = kwargs.get('published_year')
            where_clause = True
        if 'book_idx' in kwargs and kwargs.get('book_idx') is not None:
            if where_clause:
                where_query += f' {filter_operation} '
            where_query += f' book_idx = %(book_idx)s '
            query_param['book_idx'] = kwargs.get('book_idx')
            where_clause = True
        if where_clause:
            query = query + 'AND (' + where_query + ')'

        query += ' order by book_idx'.format()
        db_resp = self.execute_read_query(query=query,
                                          query_param=query_param,
                                          verbose=True)
        formatted_db_resp = await self.format_db_resp(db_resp)
        return formatted_db_resp
