DROP TABLE IF EXISTS books cascade;

CREATE TABLE books
(
    id               serial primary key,
    title            varchar(600) not null,
    author           varchar(600) not null,
    category_idx     integer,
    published_year   integer,
    price            float,
    stock_unit       integer      default 0,
    tags             varchar(600) default '<>':: character varying,
    added_user_idx   integer,
    last_modified_at timestamp    default now(),
    created_at       timestamp    default now(),
    CONSTRAINT user_book_index FOREIGN KEY (added_user_idx) REFERENCES users (id),
    CONSTRAINT category_book_index FOREIGN KEY (category_idx) REFERENCES category (id)
);

-- update last modified timestamp
CREATE
    or replace FUNCTION books_last_modified_func() RETURNS trigger AS
$$
BEGIN
    NEW.last_modified_at
        := NOW();

    RETURN NEW;
END;
$$
    LANGUAGE plpgsql;

CREATE TRIGGER
    books_last_modified_trigger
    BEFORE UPDATE
    ON
        books
    FOR EACH ROW
EXECUTE PROCEDURE books_last_modified_func();


create index title_varchar_books_index on books (title varchar_pattern_ops);
create index author_varchar_books_index on books (author varchar_pattern_ops);
create index tags_varchar_books_index on books (tags varchar_pattern_ops);

INSERT INTO books (title, author, category_idx, published_year, price, stock_unit, tags, added_user_idx)
VALUES ('The Great Gatsby', 'F. Scott Fitzgerald', 1, 1925, 12.99, 10, '<>', 1),
       ('To Kill a Mockingbird', 'Harper Lee', 3, 1983, 12.99, 0, '<>', 2),
       ('1984', 'George Orwell', 4, 1949, 9.99, 5, '<>', 1),
       ('Pride and Prejudice', 'Jane Austen', 1, 1813, 8.99, 12, '<>', 2),
       ('The Hobbit', 'J.R.R. Tolkien', 5, 1937, 14.99, 3, '<>', 2),
       ('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', 2, 1997, 11.99, 8, '<>', 1),
       ('The Catcher in the Rye', 'J.D. Salinger', 1, 1951, 10.99, 6, '<>', 1),
       ('The Alchemist', 'Paulo Coelho', 1, 1988, 7.99, 15, '<>', 2),
       ('The Lord of the Rings', 'J.R.R. Tolkien', 4, 1954, 19.99, 2, '<>', 1),
       ('The Chronicles of Narnia', 'C.S. Lewis', 2, 1950, 13.99, 4, '<>', 2),
       ('Moby-Dick', 'Herman Melville', 2, 1851, 15.99, 5, '<>', 2),
       ('Alice''s Adventures in Wonderland', 'Lewis Carroll', 2, 1865, 7.99, 20, '<>', 1),
       ('The Chronicles of Narnia', 'C.S. Lewis', 1, 1950, 19.99, 10, '<>', 2),
       ('Frankenstein', 'Mary Shelley', 6, 1818, 12.99, 15, '<>', 1),
       ('Brave New World', 'Aldous Huxley', 5, 1932, 11.99, 25, '<>', 2),
       ('The Odyssey', 'Homer', 1, 1932, 9.99, 30, '<>', 1),
       ('The Picture of Dorian Gray', 'Oscar Wilde', 1, 1890, 10.99, 20, '<>', 2),
       ('The Kite Runner', 'Khaled Hosseini', 6, 2003, 13.99, 15, '<>', 1),
       ('Gone with the Wind', 'Margaret Mitchell', 3, 1936, 16.99, 10, '<>', 2),
       ('The Hunger Games', 'Suzanne Collins', 4, 2008, 11.99, 30, '<>', 1);

