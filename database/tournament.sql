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
	player_one_id INTEGER,
	player_two_id INTEGER,
	event_id INTEGER,
	player_one_score DOUBLE PRECISION,
	player_two_score DOUBLE PRECISION,
	round_number INTEGER
);
