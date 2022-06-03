

create table users
(
    chat_id   bigint            not null
        constraint users_pk
            primary key,
    username  text,
    full_name text,
    uname     text,
    age       integer,
    regit     boolean default false,
    id        serial            not null,
    balance   integer default 0 not null
);


create unique index users_id_uindex
    on users (id);