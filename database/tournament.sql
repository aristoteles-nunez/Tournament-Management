-- Table definitions for the tournament project.
--

CREATE TABLE players (
	firstname TEXT,
	lastname TEXT,
	id SERIAL PRIMARY KEY
);

CREATE TABLE events (
	name TEXT,
	event_date TIMESTAMP,
	id SERIAL PRIMARY KEY
);

CREATE TABLE playersInEvent (
	event INTEGER REFERENCES events(id),
	player INTEGER REFERENCES players(id),
	PRIMARY KEY(event, player)
);

CREATE TABLE matches (
	player_one INTEGER REFERENCES players(id),
	player_two INTEGER REFERENCES players(id),
	player_one_score DOUBLE PRECISION,
	player_two_score DOUBLE PRECISION,
	event INTEGER REFERENCES events(id),
	round_number INTEGER,
	id SERIAL PRIMARY KEY
);

CREATE OR REPLACE FUNCTION activePlayersInEvent(actualEvent INTEGER)
RETURNS TABLE(
	id INTEGER,
	name TEXT
) AS $func$
SELECT players.id, (firstname || ' ' || lastname) as name 
        FROM players, playersInEvent WHERE event=actualEvent 
        AND players.id=playersInEvent.player;
$func$  LANGUAGE sql;


CREATE OR REPLACE FUNCTION matchesByPlayersInEvent(actualEvent INTEGER)
RETURNS TABLE(
	id INTEGER,
	name TEXT,
	score DOUBLE PRECISION,
	match INTEGER
) AS $func$
SELECT activePlayers.id, activePlayers.name, 
	CASE WHEN activePlayers.id = matches.player_one AND matches.player_one_score != null
			THEN  matches.player_one_score
        WHEN activePlayers.id = matches.player_two AND matches.player_two_score != null
        THEN matches.player_two_score
        ELSE 0.0
    END as score
	, matches.id as match 
	FROM (SELECT * FROM activePlayersInEvent(actualEvent)) as activePlayers
	LEFT JOIN matches ON (activePlayers.id = matches.player_one) or 
        (activePlayers.id = matches.player_two)
$func$  LANGUAGE sql;


CREATE OR REPLACE FUNCTION standings(actualEvent INTEGER)
RETURNS TABLE(
	id INTEGER,
	name TEXT,
	points DOUBLE PRECISION,
	matches BIGINT 
) AS $func$
SELECT id, name, SUM(matchesByPlayers.score) AS points,
		COUNT(matchesByPlayers.match) AS matches
        FROM matchesByPlayersInEvent(actualEvent) as matchesByPlayers
        GROUP BY id, name 
        ORDER BY points DESC, name ASC;
$func$  LANGUAGE sql;
        
