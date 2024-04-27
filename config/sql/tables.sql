CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

create table if not exists users
(
    id serial primary key,
    name varchar not null,
    email varchar not null,
    password varchar not null,
    role varchar,
    status bool default true
);

CREATE TABLE IF NOT EXISTS players
(
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    "user" VARCHAR NOT NULL,
    language VARCHAR(255) DEFAULT 'pt-BR'::CHARACTER VARYING,
    uuid uuid not null unique default uuid_generate_v4(),
    status BOOL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS teams
(
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    value DECIMAL(15, 2) NOT NULL,
    player_id INTEGER,
    protocol INTEGER NOT NULL UNIQUE,
    date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_player_id FOREIGN KEY (player_id) REFERENCES players (id) ON DELETE CASCADE
);

create index IF NOT EXISTS users_index_email on users (email asc);
CREATE INDEX IF NOT EXISTS teams_index_protocol ON teams (protocol ASC);
