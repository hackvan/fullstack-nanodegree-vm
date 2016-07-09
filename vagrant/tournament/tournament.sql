-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- DROP IF EXISTS CREATE DATABASE tournament;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;
CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	name TEXT,
	total_rounds INTEGER DEFAULT 0,
	total_wins   INTEGER DEFAULT 0,
	total_draws  INTEGER DEFAULT 0,
	total_loses  INTEGER DEFAULT 0,
	points       INTEGER DEFAULT 0
);

CREATE TABLE matches (
	round SERIAL PRIMARY KEY,
	id_player1 INTEGER REFERENCES players(id),
	id_player2 INTEGER REFERENCES players(id),
	id_winner  INTEGER REFERENCES players(id),
	id_loser   INTEGER REFERENCES players(id),
	is_draw    BOOLEAN DEFAULT FALSE
);
