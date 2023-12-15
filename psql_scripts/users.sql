DROP TABLE IF EXISTS users cascade;

CREATE TABLE users
(
    id               serial primary key,
    name             varchar(600)  not null,
    email            varchar(600)  not null unique,
    password         varchar(1500) not null,
    is_admin         boolean      default False,
    tags             varchar(600) default '<>':: character varying,
    last_modified_at timestamp    default now(),
    created_at       timestamp    default now()
);

-- update last modified timestamp
CREATE
    or replace FUNCTION users_last_modified_func() RETURNS trigger AS
$$
BEGIN
    NEW.last_modified_at
        := NOW();

    RETURN NEW;
END;
$$
    LANGUAGE plpgsql;

CREATE TRIGGER
    users_last_modified_trigger
    BEFORE UPDATE
    ON
        users
    FOR EACH ROW
EXECUTE PROCEDURE users_last_modified_func();

create index email_user_varchar_index on users (email varchar_pattern_ops);

-- dump test values
INSERT INTO users (name, email, password, is_admin, tags)

VALUES ('John Doe', 'john@example.com',
        '4a983c3c3799a2cd718b33ab74d4b6d869cab1de410b8c00e0467a1e94fd8710cec84ef5bf41c43f250795a47fd69828fad5d48d3a5fa4a7401da82b880898d4',
        true, '<>'),      -- HelloWorld!123
       ('Jane Smith', 'jane@example.com',
        '12e58347e774802eadf6c566db280641152a32ab18a3e6c42d26305a9d48ff8ca5fec00971dcabf5d957075ccfdb1763d9e9e4a56b13a7a7ea9aa35fbefb3c90',
        true, '<>'),      -- HelloWorld!1234
       ('Alice Johnson', 'alice@example.com',
        '4a983c3c3799a2cd718b33ab74d4b6d869cab1de410b8c00e0467a1e94fd8710cec84ef5bf41c43f250795a47fd69828fad5d48d3a5fa4a7401da82b880898d4',
        false, '<>'),     -- HelloWorld!123
       ('Bob Anderson', 'bob@example.com',
        '5b8c66f336981f242ebc9776e585e3b3a529a666a6c6de1518fc83f56e42cde074a04eb24b2f6cc36455153ccaf37e087c9389ba4f23dd9ea13265d332630f61',
        false, '<>'),     -- HelloWorld#1236
       ('Sarah Brown', 'sarah@example.com',
        '12e58347e774802eadf6c566db280641152a32ab18a3e6c42d26305a9d48ff8ca5fec00971dcabf5d957075ccfdb1763d9e9e4a56b13a7a7ea9aa35fbefb3c90',
        false, '<>'), -- HelloWorld!1234
       ('Michael Lee', 'michael@example.com',
        'c9107b90174f4edd5009fe0ccfd42d9e4a9d48456d1f0dad2a0891feaa46002ec9b4ac8f92a12eec28532a1385b661ef1e2fd7b0c7683a1a9e364dc32ca4d65a',
        false, '<>'),     -- HelloWorld!12368
       ('Emily Davis', 'emily@example.com',
        '942abb02346b6659b8e63f986fd63fff4ec91382806d575ca375d58b0318e8d4e8b5b3d4b0d7c2909f346699667428c25b40ea869aceaa4d2787a5e10a7c0546',
        false, '<>'),     -- HelloYou!12368
       ('David Wilson', 'david@example.com',
        '942abb02346b6659b8e63f986fd63fff4ec91382806d575ca375d58b0318e8d4e8b5b3d4b0d7c2909f346699667428c25b40ea869aceaa4d2787a5e10a7c0546',
        false, '<>'),     -- HelloYou!12368
       ('Olivia Taylor', 'olivia@example.com',
        '4a983c3c3799a2cd718b33ab74d4b6d869cab1de410b8c00e0467a1e94fd8710cec84ef5bf41c43f250795a47fd69828fad5d48d3a5fa4a7401da82b880898d4',
        false, '<>'),     -- HelloWorld!123
       ('Daniel Martinez', 'daniel@example.com',
        '4a983c3c3799a2cd718b33ab74d4b6d869cab1de410b8c00e0467a1e94fd8710cec84ef5bf41c43f250795a47fd69828fad5d48d3a5fa4a7401da82b880898d4',
        false, '<>'),     -- HelloWorld!123
       ('Sophia Anderson', 'sophia@example.com',
        '5b8c66f336981f242ebc9776e585e3b3a529a666a6c6de1518fc83f56e42cde074a04eb24b2f6cc36455153ccaf37e087c9389ba4f23dd9ea13265d332630f61',
        false, '<>'); -- HelloWorld#1236
