from .base_class import DatabaseBaseClass, log_and_notify


class UsersTable(DatabaseBaseClass):
    async def insert_new_user(self, name: str, email: str, password_hashed: str, is_admin: bool, tags: {}, *args,
                              **kwargs) -> None:
        log_and_notify.info(f'Adding new user with email {email} and name {name}')

        query = 'INSERT INTO {table_name} (name, email, password, is_admin, tags) VALUES (%(name)s, %(email)s, %(password)s, %(is_admin)s, %(tags)s)'.format(
            table_name=self.table_name)
        query_param = {'name': name,
                       'email': email,
                       'password': password_hashed,
                       'is_admin': is_admin,
                       'tags': self.process_tags_columns(tags)}
        self.execute_write_query(query=query, query_param=query_param)

        log_and_notify.info(f'Added new user with email {email} and name {name}')

    async def check_admin_access(self, email: str, *args, **kwargs) -> bool:
        log_and_notify.info(f'Checking admin access for user with email {email}')
        query = 'select is_admin from {table_name} where email = %(email)s'.format(table_name=self.table_name)
        query_param = {'email': email}
        db_resp = self.execute_read_query(query=query, query_param=query_param)
        values = db_resp.get('values')
        if len(values) > 0 and len(values[0]) > 0:
            return values[0][0]
        return False

    async def validate_user_email_and_password(self, email: str, password: str, *args, **kwargs) -> bool:
        log_and_notify.info(f'Checking login authentication access for user with email {email}')
        query = 'select * from {table_name} where email = %(email)s and password = %(password)s'.format(
            table_name=self.table_name)
        query_param = {'email': email,
                       'password': password}
        db_resp = self.execute_read_query(query=query,
                                          query_param=query_param)
        values = db_resp.get('values')
        if len(values) > 0 and len(values[0]) > 0: return True
        return False

    async def is_email_present(self, email: str, *args, **kwargs) -> bool:
        log_and_notify.info(f'Checking if email is present for user with email {email}')
        query = 'select * from {table_name} where email = %(email)s'.format(table_name=self.table_name)
        query_param = {'email': email}
        db_resp = self.execute_read_query(query=query, query_param=query_param)
        values = db_resp.get('values')
        if len(values) > 0 and len(values[0]) > 0:
            return True
        return False

    async def fetch_user_details(self, email: str, password: str = '', *args, **kwargs):
        log_and_notify.info(f'Fetching access for user with email {email}')
        query = 'select * from {table_name} where email = %(email)s'.format(
            table_name=self.table_name)
        query_param = {'email': email}

        db_resp = self.execute_read_query(query=query,
                                          query_param=query_param)
        formmated_db_resp = await self.format_db_resp(db_resp)
        return formmated_db_resp
