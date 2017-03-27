-- Table definitions for the tournament project.
-- Make sure the tables don't exist to avoid duplicates and errors

-- The database connection should be declared prior creating the db structure. 
\c tournament;

DROP DATABASE IF EXISTS tournament;

DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

-- Let's start making the database

CREATE DATABASE TOURNAMENT;

-- Now the tables

CREATE TABLE players (id SERIAL primary key, name TEXT);

CREATE TABLE matches (
	id SERIAL primary key,
	winner INTEGER REFERENCES players (id),
	loser INTEGER REFERENCES players (id)
	);

-- need to create standings view
    -- Returns:
    --   A list of tuples, each of which contains (id, name, wins, matches):
    --     id: the player's unique id (assigned by the database)
    --     name: the player's full name (as registered)
    --     wins: the number of matches the player has won
    --     matches: the number of matches the player has played
    -- """  make sure parenthesis are around the query and not AS piece

CREATE VIEW standings AS
SELECT players.id AS id, players.name AS name,
(SELECT count(*) FROM matches WHERE matches.winner = players.id) AS wins,
(SELECT count(*) FROM matches WHERE players.id in (winner, loser)) AS matches
FROM players GROUP BY players.id ORDER BY wins DESC;

