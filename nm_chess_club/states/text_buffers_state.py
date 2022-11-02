import curses

from . import State
from .error_state import ErrorState

class TextBuffersState(State):
    def __init__(self, database, return_constructor):
        super().__init__(database, return_constructor)

        self.fields = []

        self.cursor_location = [0, 0]

    def display(self):
        return [field[0] + field[1] for field in self.fields]

    def current_line(self):
        return self.fields[self.cursor_location[1]][1]

    def set_current_line(self, line):
        self.fields[self.cursor_location[1]][1] = line

    def handle_key(self, key):
        if key in [curses.KEY_ENTER, 10, 13]:
            self.cursor_location[1] += 1
            if self.cursor_location[1] == len(self.fields):
                self.cursor_location = [0, 0]
                # Apply changes
                try:
                    self.update()
                except Exception as e:
                    return ErrorState(e, self)
                return self.return_constructor(self.database)

        elif key in [1, curses.KEY_HOME]:
            self.cursor_location[0] = 0
        elif key in [curses.KEY_DOWN, 9]:
            self.cursor_location[1] += 1
        elif key == curses.KEY_UP:
            self.cursor_location[1] -= 1
        elif key == curses.KEY_LEFT:
            self.cursor_location[0] -= 1
        elif key == curses.KEY_RIGHT:
            self.cursor_location[0] += 1
        elif key in [330, curses.KEY_DC, curses.KEY_BACKSPACE, 127]:
            if key in [curses.KEY_BACKSPACE, 127]:
                if self.cursor_location[0]:
                    self.cursor_location[0] -= 1
                else:
                    return self
            if self.cursor_location[0] == len(self.current_line()):
                return self
            to_pop = self.cursor_location[0]
            to_pop = self.cursor_location[0]
            string_to_change = self.current_line()
            self.set_current_line(string_to_change[:to_pop] + string_to_change[to_pop + 1:])
        else:
            to_pop = self.cursor_location[0]
            string_to_change = self.fields[self.cursor_location[1]][1]
            self.set_current_line(string_to_change[:to_pop] + chr(key) + string_to_change[to_pop:])
            self.cursor_location[0] += 1

        self.cursor_location[1] = sorted([0, self.cursor_location[1], len(self.fields) - 1])[1]
        self.cursor_location[0] = sorted([0, self.cursor_location[0], len(self.current_line())])[1]

        return self

    def cursor_position(self):
        return self.cursor_location[0] + len(self.fields[self.cursor_location[1]][0]), self.cursor_location[1]

    def key_value_pairs(self):
        return {key: field[3](field[1]) for field in self.fields for key in field[2]}

    def update(self):
        raise NotImplementedError
