#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def execute(action):
    """Open a connection and a cursor and execute an action based on @action param
       @action param receives the database and the cursor instance
       After action is performed database connection is closed and data
       is return is @action returned some data."""
    db = connect()
    c = db.cursor()
    data = action(db, c)
    db.close()
    return data

def deleteMatches():
    """Remove all the match records from the database."""
    execute(lambda db, c: (
        c.execute('delete from match'),
        db.commit()
    ))

def deletePlayers():
    """Remove all the player records from the database."""
    execute(lambda db, c: (
        c.execute('delete from player'),
        db.commit()
    ))

def countPlayers():
    """Returns the number of players currently registered."""
    def countPlayers(db, c):
        c.execute('select count(id) as num from player')
        return c.fetchone()[0]
    num = execute(countPlayers)
    return num

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    execute(lambda db, c: (
        c.execute('insert into player (name) values (%s)', (name,)),
        db.commit()
    ))

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    def playerStandings(db, c):
        c.execute('select id, name, wins, matches from vw_player_standings')
        standings = [row for row in c.fetchall()]
        return standings

    return execute(playerStandings)

def registerTournament(name):
    """ creates a tournament to support multiple tournament per time """

    def registerTournament(db, c):
        c.execute ("insert into tournament (name) values (%s)", (name))
        c.fetchone(name)
        db.commit()
        c.execute ("select * from tournament where name = %s", (name))
        result = c.fetchone(name)
        return result
    return execute(registerTournament)

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    execute(lambda db, c: (
        c.execute (
            "insert into match (winner, looser) "
            "values (%s,%s)",
            (winner, loser)
        ),
        db.commit()
    ))


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
    def swissPairings(db, c):
        c.execute ("select id1, name1, id2, name2 from vw_swiss_pairings")
        pairings = [row for row in c.fetchall()]
        return pairings
    return execute(swissPairings)
