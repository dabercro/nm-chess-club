import os
import sqlite3

def filename():
    return os.path.join(os.path.dirname(__file__), 'nm_chess_club.db')

def exists():
    """
    :returns: If the chess club database exists or not.
    :rtype: bool
    """
    # TODO check that tables exist in DB too?
    return os.path.exists(filename())

def get_cursor():
    connection = sqlite3.connect(filename())
    cursor = connection.cursor()

    return (connection, cursor)
