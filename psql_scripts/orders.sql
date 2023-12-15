DROP TABLE IF EXISTS orders cascade;

CREATE TABLE orders
(
    id             serial primary key,
    user_idx       integer,
    books_idx       varchar(400) default '<>':: character varying,
    amount         float,
    last_modified_at timestamp    default now(),
    created_at     timestamp    default now(),
    CONSTRAINT user_orders_index FOREIGN KEY (user_idx) REFERENCES users (id)
);

-- update last modified timestamp
CREATE
    or replace FUNCTION orders_last_modified_func() RETURNS trigger AS
$$
BEGIN
    NEW.last_modified_at
        := NOW();

    RETURN NEW;
END;
$$
    LANGUAGE plpgsql;

CREATE TRIGGER
    order_last_modified_trigger
    BEFORE UPDATE
    ON
        orders
    FOR EACH ROW
EXECUTE PROCEDURE orders_last_modified_func();


create index user_orders_index on orders (user_idx);
create index books_idx_orders_index on orders (books_idx varchar_pattern_ops);

