-- auto-generated definition
drop view if exists book_category_view;

create or replace view book_category_view
as
SELECT book_table.id as book_idx,
       book_table.title,
       book_table.author,
       book_table.category_idx,
       category_table.name as category_name,
       book_table.published_year,
       book_table.price,
       book_table.stock_unit,
       book_table.tags,
       book_table.added_user_idx,
       book_table.last_modified_at,
       book_table.created_at
FROM books book_table LEFT JOIN category category_table ON book_table.category_idx = category_table.id;

alter table book_category_view
    owner to library_api_superuser;

