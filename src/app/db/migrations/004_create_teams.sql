create table if not exists teams (
  id serial primary key,
  name varchar not null unique,
  price decimal(15, 2) not null,
  owner varchar not null,
  protocol integer not null unique,
  date timestamp with time zone not null default current_timestamp
);

