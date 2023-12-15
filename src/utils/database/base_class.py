from src.config import config, log_and_notify
from src.utils.database.helper import *
from src.utils.exceptions import *

import json
import psycopg2 as psycopg

database_delimiter = '<>'


class DatabaseBaseClass:

    def __init__(self, db_name: str, table_name: str, **kwargs):
        """
        Base Class for all database table where db_name, table_name are passed that will be read from service config
        :param db_name: Database Name
        :param table_name: Table Name
        :param kwargs: Keyword Arguments
        """
        self.db_config = config[db_name]
        self.host = kwargs.get('host', self.db_config.get('host', 'localhost'))
        self.port = kwargs.get('port', self.db_config.get('port', 5432))
        self.db_name = self.db_config['db_name']
        self.schema_name = self.db_config.get(
            'schema_name', 'public')  # default schema is set to public
        self.read_username = None
        self.write_username = None
        self.table_config = None
        self.read_cur = None
        self.read_conn = None
        self.write_cur = None
        self.write_conn = None
        if table_name in self.db_config['tables_config']:
            self.table_config = self.db_config['tables_config'][table_name]
            self.table_name = self.schema_name + '.' + self.table_config[
                'table_name']
            if 'read_user_config' in self.table_config:  # to perform only read operation
                self.read_username = self.table_config['read_user_config'][
                    'username']
                self.read_password = self.table_config['read_user_config'][
                    'password']

            if 'write_user_config' in self.table_config:  # to perform insert and update operation
                self.write_username = self.table_config['write_user_config'][
                    'username']
                self.write_password = self.table_config['write_user_config'][
                    'password']
            self.db_write = self.table_config.get('db_write_enable', False)
        self.complete_table_name = f'{self.db_name}.{self.table_name}'
        self.data_class = kwargs.get('data_class')
        self.start_connection()

    def start_connection(self) -> None:
        """
        Function call to start database connection for the given [table_name, db_name]
        exception will raise if table or db is not present.
        :return:
        """
        if self.table_name is not None:
            if self.read_username is not None:
                read_db_conn = psycopg.connect(database=self.db_name,
                                               user=self.read_username,
                                               password=self.read_password,
                                               host=self.host,
                                               port=self.port)

                self.read_conn = read_db_conn
                self.read_cur = self.read_conn.cursor()
                log_and_notify.info(
                    f'Read Connection established with {self.complete_table_name} for {self.read_username}'
                )

            if self.write_username is not None:
                write_db_conn = psycopg.connect(database=self.db_name,
                                                user=self.write_username,
                                                password=self.write_password,
                                                host=self.host,
                                                port=self.port)

                log_and_notify.info(
                    f'Write Connection established with {self.db_name} for {self.write_username}'
                )

                self.write_conn = write_db_conn
                self.write_cur = self.write_conn.cursor()
            if self.read_username is None and self.write_username is None:
                raise DatabaseException(
                    f'No Username and password were passed for {self.complete_table_name}'
                )
        else:
            raise DatabaseException(
                f'Table Name {self.table_name} is not present in config for {self.complete_table_name}'
            )

    def execute_read_query(self, query: str, query_param: dict, *args,
                           **kwargs) -> dict:
        """
        Function to execute read query where in query and query_param are present.
        In case user want to print the exact query pass verbose = True in kwaargs
        :param query: Datbase Query
        :param query_param: Query param {}
        :param args: Additional python argument
        :param kwargs: Additional Keyword argument {"verbose": False}
        :return:  {"header": [], 'values' : []}
        """
        original_query = None
        if self.read_username is None:
            raise DatabaseException(
                f'No read user is present for {self.complete_table_name}')
        try:
            original_query = self.read_cur.mogrify(query, query_param)
            if kwargs.get('verbose', False):
                log_and_notify.info(
                    f'Read query for {self.complete_table_name} >>> \n{original_query}'
                )
            self.read_cur.execute(query, query_param)
            values = self.read_cur.fetchall()
            header = [desc[0] for desc in self.read_cur.description]
            return {'header': header, 'values': values}
        except Exception as ex:
            log_and_notify.exception(
                f'Error occurred while running query for {self.complete_table_name} >> \n {original_query}'
            )
            self.read_conn.rollback()
            raise DatabaseException(
                'Error occurred while running query, Please contact dev team')

    def execute_write_query(self,
                            query,
                            query_param,
                            commit=True,
                            *args,
                            **kwargs):
        original_query = None
        if self.write_username is None:
            raise DatabaseException(
                f'No write user is present for {self.complete_table_name}')
        try:
            original_query = self.write_cur.mogrify(
                query, query_param)  # syntax check
            if kwargs.get('verbose', False):
                log_and_notify.info(
                    f'Write query for {self.complete_table_name} >>> {original_query}'
                )
            self.write_cur.execute(query, query_param)
            if commit:
                self.write_conn.commit()
        except Exception as ex:
            log_and_notify.exception(
                f'Error occurred while running write query for {self.complete_table_name} >>\n {original_query}'
            )
            self.rollback()
            raise DatabaseException(
                'Error occurred while running query, Please contact dev team')

    def rollback(self):
        """
        Rollback all table connetion created during init
        :return:
        """
        try:
            log_and_notify.info(
                f'Connection rollback for table {self.table_name}')
            self.read_conn.rollback()
            self.write_conn.rollback()
        except psycopg.OperationalError as exec:
            log_and_notify.exception("Multiple Rollback")

    def process_tags_columns(self, tags: dict) -> str:
        log_and_notify.info(f'Processing tag {tags}')
        output_string = f'{database_delimiter}'
        for key, value in tags.items():
            output_string += f'{key}:{value}{database_delimiter}'
        return output_string

    async def format_db_resp(self, db_resp: dict):
        db_formatted_resp = []
        if self.data_class is not None:
            header = db_resp.get('header', [])
            values = db_resp.get('values', [])
            for single_db_resp in values:
                data_obj = self.data_class(header, single_db_resp)
                db_formatted_resp.append(data_obj)
        else:
            return db_resp
        return db_formatted_resp
