create table if not exists users (
  id serial primary key,
  name varchar not null,
  email varchar not null,
  password varchar not null,
  role varchar,
  status bool default true
);

