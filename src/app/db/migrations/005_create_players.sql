create table if not exists players (
  id serial primary key,
  name varchar not null,
  language varchar(255) default 'pt-br'::character varying,
  uuid uuid not null unique default uuid_generate_v4(),
  status bool default false,
  team_id integer not null,
  constraint fk_team_id foreign key (team_id) references teams (id) on delete cascade
);

