-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- Database:
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;
-- Schema:
-- DROP TABLE IF EXISTS matches;
-- DROP TABLE IF EXISTS players;
-- DROP VIEW IF EXISTS players_standings;

CREATE TABLE players (
	id   SERIAL PRIMARY KEY,
	name TEXT
);
CREATE TABLE matches (
	round      SERIAL PRIMARY KEY,
	id_winner  INTEGER REFERENCES players(id),
	id_loser   INTEGER REFERENCES players(id),
	is_tie     BOOLEAN DEFAULT FALSE
);
CREATE VIEW players_standings AS 
    SELECT   p.id,
	         p.name,
             (SELECT COUNT(*) FROM matches AS m WHERE m.id_winner = p.id ) as wins,
			 (SELECT COUNT(*) FROM matches AS m WHERE m.id_loser = p.id ) as loses,
             (SELECT COUNT(*) FROM matches AS m WHERE p.id in (m.id_winner, m.id_loser) AND m.is_tie) as ties,
			 (SELECT COUNT(*) FROM matches AS m WHERE p.id in (m.id_winner, m.id_loser)) as matches
    FROM     players AS p
    GROUP BY p.id
    ORDER BY wins DESC;