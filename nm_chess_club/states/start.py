import curses

from . import State
from .add_player import AddPlayerState
from .create_matches import CreateMatchesState
from .test_keys import TestKeysState

class StartState(State):

    def __init__(self, database):
        super().__init__(database)
        self.options = [
            ('Add a new player', AddPlayerState),
            ('Generate new matches', CreateMatchesState),
            ('Test Keys', TestKeysState)
        ]
        self.buffer = ''

    def display(self):
        return ['%i: %s' % (index + 1, option[0]) for index, option in enumerate(self.options)] + \
            ['', 'Please selection an option:', self.buffer]
            
    def handle_key(self, key):
        if key in [curses.KEY_ENTER, 10, 13] and self.buffer:
            constructor = self.options[int(self.buffer) - 1][1]
            return constructor(self.database, StartState)

        elif key in [curses.KEY_BACKSPACE, 127]:
            if self.buffer:
                self.buffer = self.buffer[:-1]
        else:
            self.buffer += chr(key)

        return self

    def cursor_position(self):
        return len(self.buffer), len(self.options) + 2

    def running(self):
        return True
