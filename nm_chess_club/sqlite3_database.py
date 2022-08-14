import os
import sqlite3

class DataBase(object):

    def __init__(self, connection_params):
        self.filename = connection_params.get(
            'filename',
            os.path.join(os.path.dirname(__file__), 'nm_chess_club.db')
        )

        self.connection = None
        self.cursor = None

    def __del__(self):
        if self.connection is not None:
            self.connection.commit()
            self.connection.close()

    def exists(self):
        """
        :returns: If the chess club database exists or not.
        :rtype: bool
        """
        # TODO check that tables exist in DB too?
        return os.path.exists(self.filename)

    def get_cursor(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.filename)
            self.cursor = self.connection.cursor()

        return self.cursor
