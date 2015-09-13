#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def test_delete_all_event(test_num):
    delete_all_events()
    c = count_events()
    if type(c) is not long:
        raise TypeError(
            "count_events() should return long value.")
    if c != 0:
        raise ValueError("After deleting, count_events should return zero.")
    print ("{}. All events can be deleted.").format(test_num)

def test_delete_one_event(test_num):
    delete_all_events()
    event_id = register_event("Blitz Tournament", "2015/12/30")
    delete_event(event_id)
    event_id = register_event("Blitz Tournament2", "2015/12/30")
    c = count_events()
    if type(c) is not long:
        raise TypeError(
            "count_events() should return long value.")
    if c != 1:
        raise ValueError("After deleting, count_events should return one.")
    print ("{}. One event can be deleted.").format(test_num)
        
def test_register_event(test_num):
    delete_all_events()
    register_event("Blitz Tournament", "2015/12/30")
    c = count_events()
    if type(c) is not long:
        raise TypeError(
            "count_events() should return a long value.")
    if c != 1:
        raise ValueError("After one event registered, count_events should \
            return one.")
    print ("{}. After registering an event, count_events() returns 1.")\
            .format(test_num)

def test_delete_players(test_num):
    delete_players()
    c = count_players()
    if type(c) is not long:
        raise TypeError(
            "count_players() should return long value.")
    if c != 0:
        raise ValueError("After deleting, count_players should return zero.")
    print ("{}. All players can be deleted.").format(test_num)

def test_register_player(test_num):
    delete_players()
    register_player("Aristoteles", "Nunez")
    c = count_players()
    if type(c) is not long:
        raise TypeError(
            "count_players() should return long value.")
    if c != 1:
        raise ValueError(
            "After one player registers, count_players() should be 1.")
    print ("{}. After registering a player, count_players() returns 1.")\
            .format(test_num)

def test_add_player_to_event(test_num):
    delete_all_events()
    delete_players()
    event_id = register_event("Blitz Tournament", "2015/12/30")
    player_id = register_player("Aristoteles", "Nunez")
    add_player_to_event(event_id, player_id)
    c = count_players_in_event(event_id)
    if type(c) is not long:
        raise TypeError(
            "count_players() should return long value.")
    if c != 1:
        raise ValueError(
            "After one player adds to an event, count_players_in_event() should be 1.")
    print ("{}. After adding a player, count_players_in_event() returns 1.")\
            .format(test_num)


def test_remove_player_from_event(test_num):
    delete_all_events()
    delete_players()
    event_id = register_event("Blitz Tournament", "2015/12/30")
    player_id = register_player("Aristoteles", "Nunez")
    add_player_to_event(event_id, player_id)
    remove_player_from_event(event_id, player_id)
    c = count_players_in_event(event_id)
    if type(c) is not long:
        raise TypeError(
            "count_players() should return long value.")
    if c != 0:
        raise ValueError(
            "count_players_in_event() should be 0.")
    print ("{}. After removing a player, count_players_in_event() returns 0.")\
            .format(test_num)

def test_delete_all_matches(test_num):
    delete_all_events()
    delete_all_matches()
    print ("{}. All matches can be deleted.").format(test_num)



def test_delete_matches_from_event(test_num):
    delete_all_events()
    delete_matches_from_event()
    print ("{}. All matches from event can be deleted.").format(test_num)


def test_delete(test_num):
    delete_matches()
    delete_players()
    print ("{}. Player records can be deleted.").format(test_num)


def test_count(test_num):
    delete_matches()
    delete_players()
    c = count_players()
    if c == '0':
        raise TypeError(
            "count_players() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, count_players should return zero.")
    print ("{}. After deleting, count_players() returns zero.")\
            .format(test_num)


def test_register(test_num):
    delete_matches()
    delete_players()
    register_player("Chandra Nalaar")
    c = count_players()
    if c != 1:
        raise ValueError(
            "After one player registers, count_players() should be 1.")
    print ("{}. After registering a player, count_players() returns \
        1.").format(test_num)


def test_register_count_delete(test_num):
    delete_matches()
    delete_players()
    register_player("Markov Chaney")
    register_player("Joe Malik")
    register_player("Mao Tsu-hsi")
    register_player("Atlanta Hope")
    c = count_players()
    if c != 4:
        raise ValueError(
            "After registering four players, count_players should be 4.")
    delete_players()
    c = count_players()
    if c != 0:
        raise ValueError("After deleting, count_players should return zero.")
    print ("{}. Players can be registered and deleted.").format(test_num)


def test_standings_before_matches(test_num):
    delete_matches()
    delete_players()
    register_player("Melpomene Murray")
    register_player("Randy Schwartz")
    standings = player_standings()
    if len(standings) < 2:
        raise ValueError("Players should appear in player_standings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each player_standings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print ("{}. Newly registered players appear in the standings with no \
        matches.").format(test_num)


def test_report_matches(test_num):
    delete_matches()
    delete_players()
    register_player("Bruno Walton")
    register_player("Boots O'Neal")
    register_player("Cathy Burton")
    register_player("Diane Grant")
    standings = player_standings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    report_match(id1, id2)
    report_match(id3, id4)
    standings = player_standings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print ("{}. After a match, players have updated standings.")\
            .format(test_num)


def test_pairings(test_num):
    delete_matches()
    delete_players()
    register_player("Twilight Sparkle")
    register_player("Fluttershy")
    register_player("Applejack")
    register_player("Pinkie Pie")
    standings = player_standings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    report_match(id1, id2)
    report_match(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print ("{}. After one match, players with one win are paired.")\
            .format(test_num)


if __name__ == '__main__':
    test_delete_all_event(1)
    test_delete_one_event(2)
    test_register_event(3)
    test_delete_players(4)
    test_register_player(5)
    test_add_player_to_event(6)
    test_remove_player_from_event(7)
    test_delete_all_matches(8)
    test_delete_matches_from_event(9)
    test_delete(6)
    test_count(7)
    test_register(8)
    test_register_count_delete(9)
    test_standings_before_matches(10)
    test_report_matches(11)
    test_pairings(12)
    print "Success!  All tests pass!"


