create extension if not exists "uuid-ossp";

create table if not exists users (
  id serial primary key,
  name varchar not null,
  email varchar not null,
  password varchar not null,
  role varchar,
  status bool default true
);

create table if not exists players (
  id serial primary key,
  name varchar not null,
  "user" varchar not null,
  language varchar(255) default 'pt-br'::character varying,
  uuid uuid not null unique default uuid_generate_v4(),
  status bool default false
);

create table if not exists teams (
  id serial primary key,
  name varchar not null unique,
  value decimal(15, 2) not null,
  player_id integer,
  protocol integer not null unique,
  date timestamp with time zone not null default current_timestamp,
  constraint fk_player_id foreign key (player_id) references players (id) on delete cascade
);

create index if not exists users_index_email on users (email asc);
create index if not exists teams_index_protocol on teams (protocol asc);
