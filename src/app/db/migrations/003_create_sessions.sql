create table if not exists sessions (
    id serial primary key,
    access_token text not null,
    user_agent text,
    ip varchar,
    revoked bool default false,
    user_id integer not null,
    constraint fk_user_id foreign key (user_id) references users (id) on delete cascade,
    date timestamp with time zone not null default current_timestamp
);

