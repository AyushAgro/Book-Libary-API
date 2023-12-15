from src.utils.exceptions import (CategoryNameNotFoundException,
                                  DatabaseException)

from .base_class import DatabaseBaseClass, log_and_notify


class CategoryTable(DatabaseBaseClass):

    async def fetch_all_avilable_category(self):
        log_and_notify.info(f'Fetching all category from {self.table_name}')
        query = 'select * from {table_name} where active = true'.format(
            table_name=self.table_name)
        query_param = {}
        db_resp = self.execute_read_query(query=query, query_param=query_param)
        formatted_db_resp = await self.format_db_resp(db_resp)
        return formatted_db_resp

    async def is_category_present(self,
                                  category_name=None,
                                  category_idx=None) -> bool:
        if category_name is not None:
            log_and_notify.info(
                f'Checking if category {category_name} is presnet')
            query = 'select * from {table_name} where name = %(name)s and active = true'.format(
                table_name=self.table_name)
            query_param = {'name': category_name}
        elif category_idx is not None:
            log_and_notify.info(
                f'Checking if category {category_idx} is presnet')
            query = 'select * from {table_name} where id = %(category_idx)s and active = true'.format(
                table_name=self.table_name)
            query_param = {'category_idx': category_idx}
        else:
            raise DatabaseException(
                'Pass category name or category index to check wheather category exist'
            )
        db_resp = self.execute_read_query(query=query, query_param=query_param)
        values = db_resp.get('values')
        if len(values) > 0 and len(values[0]) > 0: return True
        return False

    async def get_category_id(self, category_name) -> int:
        log_and_notify.info(f'Checking if category {category_name} is presnet')
        query = 'select id from {table_name} where name = %(name)s and active = true'.format(
            table_name=self.table_name)
        query_param = {'name': category_name}
        db_resp = self.execute_read_query(query=query, query_param=query_param)
        values = db_resp.get('values')
        if len(values) > 0 and len(values[0]) > 0:
            return values[0][0]
        else:
            raise CategoryNameNotFoundException(category_name)

    async def delete_category(self, category_name) -> None:
        log_and_notify.info(
            f'Deleting category {category_name} from {self.table_name}')
        query = 'delete from {table_name} where name = %(name)s and active = true'.format(
            table_name=self.table_name)
        query_param = {'name': category_name}
        self.execute_write_query(query=query, query_param=query_param)

    async def update_category(self, old_category_name,
                              new_category_name) -> None:
        log_and_notify.info(
            f'Updating category name from {old_category_name} to {new_category_name}'
        )

        query = 'update {table_name} set name = %(new_category_name)s where name = %(old_category_name)s and active = true'.format(
            table_name=self.table_name)
        query_param = {
            'old_category_name': old_category_name,
            'new_category_name': new_category_name
        }
        self.execute_write_query(query=query, query_param=query_param)

    async def insert_new_category(self, name, added_user_idx) -> None:
        log_and_notify.info(
            f'Inserting new category {name} for user {added_user_idx}')
        query = 'INSERT INTO {table_name} (name, added_user_idx) values (%(name)s, %(added_user_idx)s )'.format(
            table_name=self.table_name)
        query_param = {'name': name, 'added_user_idx': added_user_idx}
        self.execute_write_query(query=query, query_param=query_param)
