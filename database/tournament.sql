-- Table definitions for the tournament project.
--

-- Containtais all the players registered in database
-- It stores the lastname and firstname separately 
-- to allows diferents orders
CREATE TABLE players (
	firstname TEXT,
	lastname TEXT,
	id SERIAL PRIMARY KEY
);


-- Table Events has every tournament record
-- It is possible to add a future event for event_date
CREATE TABLE events (
	name TEXT,
	event_date TIMESTAMP,
	id SERIAL PRIMARY KEY
);


-- Table Players in Event specifies the relation between 
-- the registered player and the current event
CREATE TABLE playersInEvent (
	event INTEGER REFERENCES events(id),
	player INTEGER REFERENCES players(id),
	PRIMARY KEY(event, player)
);


-- Table Matches stores every match among players
-- It allows to store the round number,
-- player order (if we can implement white and black order for chess)
-- and the points granted for each player
CREATE TABLE matches (
	player_one INTEGER REFERENCES players(id),
	player_two INTEGER REFERENCES players(id),
	player_one_score DOUBLE PRECISION,
	player_two_score DOUBLE PRECISION,
	event INTEGER REFERENCES events(id),
	round_number INTEGER,
	id SERIAL PRIMARY KEY
);


-- Stored procedure: Active Players In Event
-- determines which players are in the current event
-- and puts togther the full name
CREATE OR REPLACE FUNCTION activePlayersInEvent(currentEvent INTEGER)
RETURNS TABLE(
	id INTEGER,
	name TEXT
) AS $func$
SELECT players.id, (firstname || ' ' || lastname) as name 
        FROM players, playersInEvent WHERE event=currentEvent 
        AND players.id=playersInEvent.player;
$func$  LANGUAGE sql;


-- Stored procedure: Matches by players in the current event
-- It performs a left join between the active players in the curren event
-- and the stored matches
-- For every match we select the right score deppending of the player order
-- in that match, if None we set it to zero
CREATE OR REPLACE FUNCTION matchesByPlayersInEvent(currentEvent INTEGER)
RETURNS TABLE(
	id INTEGER,
	name TEXT,
	score DOUBLE PRECISION,
	match INTEGER
) AS $func$
SELECT activePlayers.id, activePlayers.name, 
	CASE WHEN activePlayers.id = matches.player_one 
			THEN  matches.player_one_score
        WHEN activePlayers.id = matches.player_two 
        THEN matches.player_two_score
        ELSE 0.0
    END as score
	, matches.id as match 
	FROM (SELECT * FROM activePlayersInEvent(currentEvent)) as activePlayers
	LEFT JOIN matches ON (activePlayers.id = matches.player_one) or 
        (activePlayers.id = matches.player_two)
$func$  LANGUAGE sql;


-- Store procedure: Standings
-- It has aggregation functions to determine:
-- number of matches and total points earned in that matches
CREATE OR REPLACE FUNCTION standings(currentEvent INTEGER)
RETURNS TABLE(
	id INTEGER,
	name TEXT,
	points DOUBLE PRECISION,
	matches BIGINT 
) AS $func$
SELECT id, name, SUM(matchesByPlayers.score) AS points,
		COUNT(matchesByPlayers.match) AS matches
        FROM matchesByPlayersInEvent(currentEvent) as matchesByPlayers
        GROUP BY id, name 
        ORDER BY points DESC, name ASC;
$func$  LANGUAGE sql;
        
