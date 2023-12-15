DROP TABLE IF EXISTS cart cascade;

--Note: users can buy multiple copy of a book,
CREATE TABLE cart
(
    id               serial primary key,
    user_idx         integer not null,
    book_idx         integer not null,
    price            decimal not null,
    added_time       timestamp default now(),
    removal_time     timestamp default now() + (30 * interval '1 minute'),
    expired          boolean   default false,
    last_modified_at timestamp default now(),
    created_at       timestamp default now(),
    CONSTRAINT user_cart_index FOREIGN KEY (user_idx) REFERENCES users (id),
    CONSTRAINT book_cart_index FOREIGN KEY (book_idx) REFERENCES books (id) ON DELETE CASCADE,
    UNIQUE (user_idx, book_idx)
);


-- update last modified timestamp
CREATE
    or replace FUNCTION cart_last_modified_func() RETURNS trigger AS
$$
BEGIN
    NEW.last_modified_at
        := NOW();

    RETURN NEW;
END;
$$
    LANGUAGE plpgsql;

CREATE TRIGGER
    cart_last_modified_trigger
    BEFORE UPDATE
    ON
        cart
    FOR EACH ROW
EXECUTE PROCEDURE cart_last_modified_func();

create index user_cart_index on cart (user_idx);
create index removal_time_cart_index on cart (removal_time);
create index expired_cart_index on cart (expired);


INSERT INTO cart (user_idx, book_idx, price, added_time, removal_time)
VALUES (1, 1, 11.99, NOW() + INTERVAL '100 minutes', NOW() + INTERVAL '130 minutes'),
       (1, 2, 15.99, NOW() + INTERVAL '105 minutes', NOW() + INTERVAL '135 minutes'),

       (2, 10, 16.99, NOW() + INTERVAL '95 minutes', NOW() + INTERVAL '125 minutes'),

       (3, 1, 12.99, NOW(), NOW() + INTERVAL '30 minutes'),
       (3, 2, 7.99, NOW() + INTERVAL '50 minutes', NOW() + INTERVAL '80 minutes'),
       (3, 3, 11.99, NOW() + INTERVAL '15 minutes', NOW() + INTERVAL '45 minutes'),
       (3, 4, 9.99, NOW() + INTERVAL '30 minutes', NOW() + INTERVAL '60 minutes'),
       (3, 5, 13.99, NOW() + INTERVAL '90 minutes', NOW() + INTERVAL '120 minutes'),

       (4, 5, 10.99, NOW() + INTERVAL '20 minutes', NOW() + INTERVAL '50 minutes'),
       (4, 2, 9.99, NOW() + INTERVAL '5 minutes', NOW() + INTERVAL '35 minutes'),
       (4, 10, 15.99, NOW() + INTERVAL '45 minutes', NOW() + INTERVAL '75 minutes'),
       (4, 1, 19.99, NOW() + INTERVAL '55 minutes', NOW() + INTERVAL '85 minutes'),

       (5, 3, 14.99, NOW() + INTERVAL '10 minutes', NOW() + INTERVAL '40 minutes'),
       (5, 6, 13.99, NOW() + INTERVAL '25 minutes', NOW() + INTERVAL '55 minutes'),
       (5, 2, 12.99, NOW() + INTERVAL '60 minutes', NOW() + INTERVAL '90 minutes'),

       (6, 8, 24.99, NOW() + INTERVAL '35 minutes', NOW() + INTERVAL '65 minutes'),
       (6, 4, 11.99, NOW() + INTERVAL '65 minutes', NOW() + INTERVAL '95 minutes'),

       (7, 9, 8.99, NOW() + INTERVAL '40 minutes', NOW() + INTERVAL '70 minutes'),
       (7, 5, 13.99, NOW() + INTERVAL '70 minutes', NOW() + INTERVAL '100 minutes'),

       (8, 6, 16.99, NOW() + INTERVAL '75 minutes', NOW() + INTERVAL '105 minutes'),
       (9, 7, 11.99, NOW() + INTERVAL '80 minutes', NOW() + INTERVAL '110 minutes'),
       (10, 8, 10.99, NOW() + INTERVAL '85 minutes', NOW() + INTERVAL '115 minutes');
