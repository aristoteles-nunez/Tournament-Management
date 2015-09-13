#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import psycopg2.extras


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def crud_operation(operation, query, params, expected_rows, return_id):
    rows = None
    db = connect()
    c = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    c.execute(query, params)
    if operation == "read":
        rows = c.fetchone() if expected_rows == "one" else c.fetchall()
    else:
        if operation == "create" and return_id:
            rows = c.fetchone()
        db.commit()

    db.close()
    return rows;

def delete_event(id):
    """Remove an event and all its related data from the database, without 
    erasing registered players."""
    query = "DELETE FROM events WHERE id=%s"
    crud_operation("delete", query, [id], None, None)

def delete_all_events():
    """Remove all events and all their related data from the database, 
    without erasing registered players."""
    query = "DELETE FROM events"
    crud_operation("delete", query, [], None, None)


def delete_matches():
    """Remove all the match records from the database."""


def delete_players():
    """Remove all the player records from the database."""
    query = "DELETE FROM players"
    crud_operation("delete", query, [], None, None)

def register_event(name, event_date):
    """Adds a new event to the tournament database.
  
    The database assigns a unique serial id number for the event. 
  
    Args:
      name: the event's full name (need not be unique).
      event_date: this date could be in a future time.
    """
    query = "INSERT INTO events (name, event_date) VALUES (%s, %s) RETURNING id"
    row = crud_operation("create", query, [name, event_date], None, True)
    return row["id"]

def count_events():
    """Returns the number of events currently registered."""
    query = "SELECT count(*) as num FROM events"
    row =  crud_operation("read", query, [], "one", None)
    return row["num"]


def count_players():
    """Returns the number of players currently registered."""
    query = "SELECT count(*) as num FROM players"
    row =  crud_operation("read", query, [], "one", None)
    return row["num"]


def register_player(firstname, lastname):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      firstname: the player's firstname (need not be unique).
      lastname: the player's lastname (need not be unique).
    """
    query = "INSERT INTO players (firstname, lastname) VALUES (%s, %s) RETURNING id"
    row = crud_operation("create", query, [firstname, lastname], None, True)
    return row["id"]


def add_player_to_event(event_id, player_id):
    """Adds a player into an existing event.
  
    Args:
      event_id: the id's event.
      player_id: the id's player.
    """
    query = "INSERT INTO playersInEvent (event, player) VALUES (%s, %s)"
    crud_operation("create", query, [event_id, player_id], None, False)


def player_standings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, 
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def report_match(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
 
def swiss_pairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


