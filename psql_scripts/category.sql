DROP TABLE IF EXISTS category cascade;

CREATE TABLE category
(
    id               serial primary key,
    name             varchar(600) not null unique,
    added_user_idx   integer,
    active           boolean   default true,
    last_modified_at timestamp default now(),
    created_at       timestamp default now(),
    CONSTRAINT user_book_index FOREIGN KEY (added_user_idx) REFERENCES users (id)
);

-- update last modified timestamp
CREATE
    or replace FUNCTION category_last_modified_func() RETURNS trigger AS
$$
BEGIN
    NEW.last_modified_at
        := NOW();

    RETURN NEW;
END;
$$
    LANGUAGE plpgsql;

CREATE TRIGGER
    category_last_modified_trigger
    BEFORE UPDATE
    ON
        category
    FOR EACH ROW
EXECUTE PROCEDURE category_last_modified_func();

create index category_name_varchar_index on category (name varchar_pattern_ops);

INSERT INTO category (name, added_user_idx)
VALUES ('Electronics', 1),
       ('Books', 1),
       ('Clothing', 2),
       ('Home Decor', 1),
       ('Sports & Fitness', 2),
       ('Beauty & Personal Care', 1),
       ('Toys & Games', 2),
       ('Automotive', 1),
       ('Health & Wellness', 2),
       ('Food & Beverages', 1);