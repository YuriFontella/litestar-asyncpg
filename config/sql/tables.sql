create extension if not exists "uuid-ossp";

create table if not exists users (
  id serial primary key,
  name varchar not null,
  email varchar not null,
  password varchar not null,
  role varchar,
  status bool default true
);

create table if not exists teams (
  id serial primary key,
  name varchar not null unique,
  price decimal(15, 2) not null,
  owner varchar not null,
  protocol integer not null unique,
  date timestamp with time zone not null default current_timestamp
);

create table if not exists players (
  id serial primary key,
  name varchar not null,
  language varchar(255) default 'pt-br'::character varying,
  uuid uuid not null unique default uuid_generate_v4(),
  status bool default false,
  team_id integer not null,
  constraint fk_team_id foreign key (team_id) references teams (id) on delete cascade
);

create index if not exists users_index_email on users (email asc);
create index if not exists teams_index_protocol on teams (protocol asc);
