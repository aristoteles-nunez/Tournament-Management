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
    delete_all_events()
    delete_players()
    c = count_players()
    if type(c) is not long:
        raise TypeError(
            "count_players() should return long value.")
    if c != 0:
        raise ValueError("After deleting, count_players should return zero.")
    print ("{}. All players can be deleted.").format(test_num)


def test_register_player(test_num):
    delete_all_events()
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
    event_id = register_event("Blitz Tournament", "2015/12/30")
    delete_matches_from_event(event_id)
    print ("{}. All matches from event can be deleted.").format(test_num)


def test_register_count_delete(test_num):
    delete_all_events()
    delete_all_matches()
    delete_players()
    register_player("Markov", "Chaney")
    register_player("Joe", "Malik")
    register_player("Mao", "Tsu-hsi")
    register_player("Atlanta", "Hope")
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
    delete_all_events()
    delete_all_matches()
    delete_players()
    event_id = register_event("Blitz Tournament", "2015/12/30")
    player1_id = register_player("Melpomene", "Murray")
    player2_id = register_player("Randy", "Schwartz")
    player3_id = register_player("Aristoteles", "Nunez")
    player4_id = register_player("Gary", "Nunez")
    add_player_to_event(event_id, player1_id)
    add_player_to_event(event_id, player4_id)
    standings = player_standings(event_id)
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
    if set([name1, name2]) != set(["Melpomene Murray", "Gary Nunez"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print ("{}. Newly registered players appear in the standings with no matches.")\
            .format(test_num)


def test_report_matches(test_num):
    delete_all_events()
    delete_all_matches()
    delete_players()
    event_id = register_event("Blitz Tournament", "2015/12/30")
    player1_id = register_player("Melpomene", "Murray")
    player2_id = register_player("Randy", "Schwartz")
    player3_id = register_player("Aristoteles", "Nunez")
    player4_id = register_player("Gary", "Nunez")
    add_player_to_event(event_id, player1_id)
    add_player_to_event(event_id, player2_id)
    add_player_to_event(event_id, player3_id)
    add_player_to_event(event_id, player4_id)
    standings = player_standings(event_id)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    report_match(event_id, 1, id1, 1.0, id2, 0.0)
    report_match(event_id, 1, id3, 0.0, id4, 1.0)
    standings = player_standings(event_id)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id4) and w < 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id3) and w > 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print ("{}. After a match, players have updated standings.")\
            .format(test_num)


def test_pairings(test_num):
    delete_all_events()
    delete_all_matches()
    delete_players()
    event_id = register_event("Blitz Tournament", "2015/12/30")
    player1_id = register_player("Twilight", "Sparkle")
    player2_id = register_player("Flutter", "Shy")
    player3_id = register_player("Aristoteles", "Nunez")
    player4_id = register_player("Gary", "Nunez")
    add_player_to_event(event_id, player1_id)
    add_player_to_event(event_id, player2_id)
    add_player_to_event(event_id, player3_id)
    add_player_to_event(event_id, player4_id)
    standings = player_standings(event_id)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    report_match(event_id, 1, id1, 1.0, id2, 0.0)
    report_match(event_id, 1, id3, 1.0, id4, 0.0)
    pairings = swiss_pairings(event_id)
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


def test_tournament (test_num):
    delete_all_events()
    delete_all_matches()
    delete_players()
    event_id = register_event("Blitz Tournament", "2015/12/30")
    player1_id = register_player("Twilight", "Sparkle")
    player2_id = register_player("Flutter", "Shy")
    player3_id = register_player("Aristoteles", "Nunez")
    player4_id = register_player("Gary", "Nunez")
    player5_id = register_player("Federico", "Juarez")
    player6_id = register_player("Sahadi", "Urbina")
    player7_id = register_player("Itzel", "Lopez")
    player8_id = register_player("Vladimir", "Kramnik")
    player9_id = register_player("Bobby", "Fisher")
    player10_id = register_player("Magnus", "Carlsen")
    player11_id = register_player("Emanuel", "Lasker")
    player12_id = register_player("Raul", "Capablanca")
    player13_id = register_player("Boris", "Spasky")
    player14_id = register_player("Anand", "Viswanathan")
    player15_id = register_player("Gary", "Kasparov")
    player16_id = register_player("Anatoli", "Karpov")
    add_player_to_event(event_id, player1_id)
    add_player_to_event(event_id, player2_id)
    add_player_to_event(event_id, player3_id)
    add_player_to_event(event_id, player4_id)
    add_player_to_event(event_id, player5_id)
    add_player_to_event(event_id, player6_id)
    add_player_to_event(event_id, player7_id)
    add_player_to_event(event_id, player8_id)
    add_player_to_event(event_id, player9_id)
    add_player_to_event(event_id, player10_id)
    add_player_to_event(event_id, player11_id)
    add_player_to_event(event_id, player12_id)
    add_player_to_event(event_id, player13_id)
    add_player_to_event(event_id, player14_id)
    add_player_to_event(event_id, player15_id)
    add_player_to_event(event_id, player16_id)
    standings = player_standings(event_id)
    #print ("\n{}\n".format(standings))
    pairings = swiss_pairings(event_id)
    for pair in pairings:
        (id1, name1, id2, name2) = pair
        report_match(event_id, 1, id1, 1.0, id2, 0.0)
    standings = player_standings(event_id)
    #print ("\n{}\n".format(standings))
    pairings = swiss_pairings(event_id)
    for pair in pairings:
        (id1, name1, id2, name2) = pair
        report_match(event_id, 2, id1, 1.0, id2, 0.0)
    standings = player_standings(event_id)
    #print ("\n{}\n".format(standings))
    pairings = swiss_pairings(event_id)
    for pair in pairings:
        (id1, name1, id2, name2) = pair
        report_match(event_id, 3, id1, 1.0, id2, 0.0)
    standings = player_standings(event_id)
    #print ("\n{}\n".format(standings))
    pairings = swiss_pairings(event_id)
    for pair in pairings:
        (id1, name1, id2, name2) = pair
        report_match(event_id, 4, id1, 0.0, id2, 1.0)
    standings = player_standings(event_id)
    #print ("\n{}\n".format(standings))
    for (i, n, p, m) in standings:
        if m != 4:
            raise ValueError("Each player should have 4 matches recorded.")
    (i1, n1, p1, m1) = standings[0]
    (i16, n16, p16, m16) = standings[len(standings)-1]
    if p1 < 4.0:
        raise ValueError("In this case winner must have 4 points")
    if p16 > 0.0:
        raise ValueError("In this case the last player must have 0 points")
    print ("{}. After 4 rounds we have a winner")\
            .format(test_num)


def test_prevent_rematches (test_num):
    delete_all_events()
    delete_all_matches()
    delete_players()
    event_id = register_event("Blitz Tournament", "2015/12/30")
    player1_id = register_player("Twilight", "Sparkle")
    player2_id = register_player("Flutter", "Shy")
    player3_id = register_player("Aristoteles", "Nunez")
    player4_id = register_player("Gary", "Nunez")
    player5_id = register_player("Vladimir", "Kramnik")
    player6_id = register_player("Sahadi", "Urbina")
    player7_id = register_player("Itzel", "Lopez")
    player8_id = register_player("Vladimir", "Kramnik")
    add_player_to_event(event_id, player1_id)
    add_player_to_event(event_id, player2_id)
    add_player_to_event(event_id, player3_id)
    add_player_to_event(event_id, player4_id)
    add_player_to_event(event_id, player5_id)
    add_player_to_event(event_id, player6_id)
    add_player_to_event(event_id, player7_id)
    add_player_to_event(event_id, player8_id)
    standings = player_standings(event_id)
    #print ("\n{}\n".format(standings))
    # Pairings with score 0
    pairings = swiss_pairings(event_id)
    (p1id1, p1name1, p1id2, p1name2) = pairings[0]
    for pair in pairings:
        (id1, name1, id2, name2) = pair
        report_match(event_id, 1, id1, 0.5, id2, 0.5)
    standings = player_standings(event_id)
    #print ("\n{}\n".format(standings))
    # After everybody ties, the pairings must prevent rematches
    pairings = swiss_pairings(event_id)
    #print ("\n{}\n".format(pairings))
    (p2id1, p2name1, p2id2, p2name2) = pairings[0]
    round_one = set([p1id1, p1id2])
    round_two = set([p2id1, p2id2])
    if round_one == round_two:
        raise ValueError(
            "After one match players do not rematch.")
    print ("{}. Preventing rematches between players")\
            .format(test_num)


def test_odd_players (test_num):
    delete_all_events()
    delete_all_matches()
    delete_players()
    event_id = register_event("Blitz Tournament", "2015/12/30")
    player1_id = register_player("Twilight", "Sparkle")
    player2_id = register_player("Flutter", "Shy")
    player3_id = register_player("Aristoteles", "Nunez")
    add_player_to_event(event_id, player1_id)
    add_player_to_event(event_id, player2_id)
    add_player_to_event(event_id, player3_id)
    standings = player_standings(event_id)
    pairings = swiss_pairings(event_id)
    #print ("\n{}\n".format(pairings))
    standings = player_standings(event_id)
    #print ("\n{}\n".format(standings))
    if len(standings) < 4:
        raise ValueError("In this case there must be 4 players")
    print ("{}. Player Bye Added when odd number of players")\
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
    test_register_count_delete(10)
    test_standings_before_matches(11)
    test_report_matches(12)
    test_pairings(13)
    test_tournament (14)
    test_prevent_rematches(15)
    test_odd_players(16)
    print ("Success!  All tests pass!")

