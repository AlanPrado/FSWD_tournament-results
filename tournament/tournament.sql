-- Table definitions for the tournament project.

--import file file.sql to database
--\i file.sql

--drop a database
drop database tournament;

--create a database
create database tournament;

--connect to database
\c tournament

-- create tables
create table player (
  id serial CONSTRAINT pk_player_id PRIMARY KEY,
  name varchar(255) NOT NULL
);

create table tournament (
  id serial CONSTRAINT pk_tournament_id PRIMARY KEY,
  name varchar(255) NOT NULL,
  start_date timestamp DEFAULT now(),
  end_date timestamp
);

create table tournament_player (
  id serial CONSTRAINT pk_tp_id PRIMARY KEY,
  player_id integer CONSTRAINT fk_tp_player_id  NOT NULL REFERENCES player (id),
  tournament_id integer CONSTRAINT fk_tp_tournament_id  NULL REFERENCES tournament (id) ON DELETE CASCADE
);

create table match (
  id serial CONSTRAINT pk_match_id PRIMARY KEY,
  winner integer CONSTRAINT fk_match_winner NOT NULL REFERENCES player (id),
  looser integer CONSTRAINT fk_match_looser  NOT NULL REFERENCES player (id),
  --tournament_id integer CONSTRAINT fk_tournament_id  NOT NULL REFERENCES tournament (id) ON DELETE CASCADE
  tournament_id integer CONSTRAINT fk_tournament_id  NULL REFERENCES tournament (id) ON DELETE CASCADE
);

-- create view
create view vw_player_standings as
select p.id,
       p.name,
       tp.tournament_id,
       count(w.winner) wins,
       count(m.id) matches
from player p
left join match w on p.id = w.winner
left join tournament_player tp on p.id = tp.player_id
left join match m on p.id = m.winner or p.id = m.looser
group by p.id, p.name, tp.tournament_id
order by wins;

create view vw_swiss_pairings as
with results as (
  select p.id,
         p.name,
         tp.tournament_id,
         count(w.winner) wins,
         count(l.looser) looses
  from player p
  left join tournament_player tp on p.id = tp.player_id
  left join match w on p.id = w.winner --and w.tournament_id = tp.tournament_id
  left join match l on p.id = l.looser --and l.tournament_id = tp.tournament_id
  group by p.id, p.name, tp.tournament_id
  order by wins desc, looses
)
, pair_results as (
    select row_number() over() / 2 + row_number() over() % 2 pair,
           r.*
    from results r
)
select p1.id id1,
       p1.name name1,
       p2.id id2,
       p2.name name2,
       p2.tournament_id
from pair_results p2
join pair_results p1 on p1.pair = p2.pair
    and p1.id < p2.id
    ;--and p1.tournament_id = p2.tournament_id;
