create database books_library_dev;
create database books_library_prod;


create user library_api_superuser with encrypted password 'FqyVX7689oGqfu';
create user library_api_readuser with encrypted password 'ctrXEwK4b9BBVc';
create user library_api_writeuser with encrypted password '6WysfNceDXvjA4';


 -- GRANT ALL PERMISSION TO SUPERUSER
GRANT ALL PRIVILEGES ON DATABASE books_library_dev to library_api_superuser;

-- GRANT USAGE ON ALL SCHEMA OF PUBLIC
grant usage on schema public to library_api_readuser;
grant usage on schema public to library_api_writeuser;


-- grant required permission to user
GRANT SELECT ON ALL TABLES IN SCHEMA public to library_api_readuser;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public to library_api_writeuser;


grant update, insert, select, delete on category_id_seq to library_api_writeuser;
grant update, insert, select, delete on books_id_seq to library_api_writeuser;
grant update, insert, select, delete on cart_id_seq to library_api_writeuser;
grant update, insert, select, delete on orders_id_seq to library_api_writeuser;
grant update, insert, select, delete on users_id_seq to library_api_writeuser;