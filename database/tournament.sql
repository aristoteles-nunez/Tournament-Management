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
	round_number INTEGER
);
