#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "DELETE FROM matches"
    db_cursor.execute(query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "DELETE FROM players"
    db_cursor.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "SELECT count(*) FROM players"
    db_cursor.execute(query)
    # no need to commit if we're not inserting
    # get rows from db     # why rows[0][0]???
    rows = db_cursor.fetchall()[0][0]
    conn.close()
    # return the number of players registered
    return rows


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    db_cursor = conn.cursor()
    db_cursor.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    db_cursor = conn.cursor()
    query = "SELECT id, name, wins, matches FROM standings ORDER BY wins DESC;"
    db_cursor.execute(query)
    rows = db_cursor.fetchall()
    conn.close()
    # return list of tuples
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    db_cursor = conn.cursor()
    # using db_cursor.execute (query) gives TypeError: argument 1 must be
    # a string or unicode object
    db_cursor.execute(
        "INSERT INTO matches (winner, loser)VALUES (%s , %s)", (winner, loser,)
        )

    conn.commit()
    conn.close()
    # no need to return anything. Just commit


def swissPairings():
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
    # 1.get standings (already ordered via win count in playerStandings())
    # 2. Create some way to store pairings
    # 3. there will be an even number of people with the same win count
    # & loss count, until the last match, so we can break it up into
    # groups of two without worrying about remainders. Loop through
    # the standings in sets of two
    # 4. get the id and name of each two players
    # 5. add this info to the list of pairings
    # 6. return a list pairings

    standings = playerStandings()

    # empty array for pairings
    swiss_pairings = []

    # for each set of pairs **range([start], stop[, step])**
    for i in range(0, countPlayers(), 2):
        # pair up the players who have the same ranking (next to one another)
        # [0] is id, [1] is name, [i] is first player in range,
        # [i+1] is 2nd player in range
        new_matches = (
            standings[i][0], standings[i][1],
            standings[i+1][0], standings[i+1][1]
            )
        swiss_pairings.append(new_matches)

    # return a list of pairings (id1, name1, id2, name2)
    return swiss_pairings