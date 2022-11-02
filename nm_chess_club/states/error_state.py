import curses

from . import State

class ErrorState(State):
    def __init__(self, error, return_state):
        self.error = error
        self.return_state = return_state

    def display(self):
        return [str(self.error), '', 'Hit ENTER to return to previous screen']

    def handle_key(self, key):
        if key in [curses.KEY_ENTER, 10, 13]:
            return self.return_state
        return self
