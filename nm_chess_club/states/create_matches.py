import curses
import time
import random

from . import State
from .error_state import ErrorState

from ..sql_edit import update_table


def pair_off(players):
    # I'm sure there's a much better algorithm for this,
    # so rating is passed in as well
    random.shuffle(players)

    output = []
    for index in range(0, len(players) - 1, 2):
        output.append({'black': players[index], 'white': players[index + 1]})
    return output


class Player(object):
    def __init__(self, id, first, last, rating):
        self.id = id
        self.first = first
        self.last = last
        self.rating = rating


class CreateMatchesState(State):
    def __init__(self, database, return_constructor):
        super().__init__(database, return_constructor)

        # Get all of the players
        curs = self.database.get_cursor()
        curs.execute('SELECT rowid, first_name, last_name, rating FROM players;')

        self.pairs = pair_off([Player(*result) for result in curs.fetchall()])

        self.date = time.strftime('%Y-%m-%d')
        self.position = len(self.date)

    def display(self):
        return sum([['Black: %s, %s' % (match['black'].last, match['black'].first),
                     'White: %s, %s' % (match['white'].last, match['white'].first), '']
                    for match in self.pairs], []) + [self.date, '', 'Hit ENTER to accept']

    def handle_key(self, key):
        if key in [curses.KEY_ENTER, 10, 13]:
            curs = self.database.get_cursor()
            curs.execute('SELECT rowid FROM statuses WHERE status = "In Progress"')
            status = curs.fetchone()[0]
            curs.execute('SELECT MAX(round) FROM match WHERE date = ?', (self.date, ))
            round = curs.fetchone()[0]
            round = round + 1 if round is not None else 0
            for pair in self.pairs:
                try:
                    update_table(curs, "INSERT", "match",
                                 {'date': self.date,
                                  'round': round,
                                  'status': status})
                    matchid = curs.lastrowid
                    update_table(curs, "INSERT", "incomplete",
                                 {'match': matchid,
                                  'black_player': pair['black'].id,
                                  'white_player': pair['white'].id})
                except Exception as e:
                    return ErrorState(e, self)
            return self.return_constructor(self.database)

        elif key in [curses.KEY_LEFT, curses.KEY_BACKSPACE, 127]:
            self.position -= 1
            if self.date[self.position] == '-':
                self.position -= 1
        elif key == curses.KEY_RIGHT:
            self.position += 1

        elif 48 <= key and key <= 57:
            self.date = self.date[:self.position] + chr(key) + self.date[self.position + 1:]
            self.position += 1

        if self.position < len(self.date) and self.date[self.position] == '-':
            self.position += 1

        return self

    def cursor_position(self):
        return self.position, len(self.display()) - 3
