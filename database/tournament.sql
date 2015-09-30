-- Table definitions for the tournament project.
--
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;


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


-- Table Pairings stores every pairing among players
-- It allows to store the round number, event, 
-- and the points granted for each player at that time
CREATE TABLE pairings (
	id1 INTEGER REFERENCES players(id),
	name1  TEXT,
	points1 DOUBLE PRECISION,
	id2 INTEGER REFERENCES players(id),
	name2 TEXT,
	points2 DOUBLE PRECISION,
	event INTEGER REFERENCES events(id),
	round_number INTEGER,
	id SERIAL PRIMARY KEY
);


-- Function: Active Players In Event
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


-- Function: Matches by players in the current event
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


-- Function: Standings
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
        
        
-- Function: Opponents
-- It has aggregation functions to determine:
-- Opponents from a specific player
CREATE OR REPLACE FUNCTION opponents(currentEvent INTEGER, playerId INTEGER)
RETURNS TABLE(
	id INTEGER,
	name TEXT
) AS $func$
SELECT opps.opponent_id as id, ap2.name
FROM activePlayersInEvent(currentEvent) as ap2 LEFT JOIN (
	SELECT ap.id as player_id,
	CASE WHEN ap.id = mt.player_one
		THEN mt.player_two
		ELSE mt.player_one
	END AS opponent_id
	FROM activePlayersInEvent(currentEvent) AS ap 
	LEFT JOIN matches AS mt 
	ON (ap.id = mt.player_one) OR (ap.id = mt.player_two) 
) AS opps ON ap2.id = opps.opponent_id WHERE opps.player_id = playerId;
$func$  LANGUAGE sql;


-- Function: Insert Pair
-- This function insert a single pair of players that will be confronting
-- Avoid rematch between players
-- We need to perform this operation for every pair of players registered
CREATE OR REPLACE FUNCTION insertPair(currentEvent INTEGER, currentRound INTEGER)
RETURNS void AS $func$
INSERT INTO pairings (id1, name1, points1, id2, name2, points2,
		 event, round_number) (
	SELECT id1, name1, points1, id2, name2, points2, 
		currentEvent, currentRound  FROM 
		(
			SELECT std1.id AS id1, std1.name AS name1, std1.points AS points1,
	   			   std2.id AS id2, std2.name AS name2, std2.points AS points2
			FROM (
				SELECT row_number() OVER () as num, *
				FROM standings(currentEvent)
			) as std1 LEFT JOIN (
				SELECT row_number() OVER () as num, *
				FROM standings(currentEvent)
			) as std2
			ON std1.id <> std2.id AND std1.num < std2.num
			WHERE std2.id NOT IN (SELECT id FROM opponents(currentEvent,std1.id))
		) as stdxstd 
		WHERE 
			id1 not in (SELECT id1 FROM pairings 
				WHERE event=currentEvent AND round_number=currentRound) AND 
			id1 not in (SELECT id2 FROM pairings
				WHERE event=currentEvent AND round_number=currentRound) AND 
			id2 not in (SELECT id1 FROM pairings
				WHERE event=currentEvent AND round_number=currentRound) AND 
			id2 not in (SELECT id2 FROM pairings
				WHERE event=currentEvent AND round_number=currentRound)
	limit 1
);
$func$  LANGUAGE sql;


-- Function: Make All Pairs
-- It makes every pair of players that will be confronting
-- We generate every pair from the number of players registered to the event
CREATE OR REPLACE FUNCTION makeAllPairs(currentEvent INTEGER, currentRound INTEGER, playersNumber INTEGER)
RETURNS TABLE(
	id1 INTEGER,
	name1 TEXT,
	id2 INTEGER,
	name2 TEXT
) AS $func$
#variable_conflict use_column
DECLARE
	x int;
BEGIN
	-- Deleting possible records if this function was called before
	DELETE FROM pairings WHERE event=currentEvent AND round_number=currentRound;
	
	-- Determining number of pairs
	x := playersNumber / 2;

	FOR i IN 1..x LOOP
		PERFORM insertPair(currentEvent, currentRound);
	END LOOP;

	-- Returning all the records for this round
	RETURN QUERY SELECT id1, name1, id2, name2
				FROM pairings 
				WHERE event = currentEvent AND
					round_number = currentRound;
END;
$func$  LANGUAGE plpgsql;

