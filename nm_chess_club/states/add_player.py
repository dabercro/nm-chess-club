import curses

from . import State

class AddPlayerState(State):
    def __init__(self, database, return_constructor):
        super().__init__(database, return_constructor)

        self.fields = [
            [' First Name: ', '', ['first_name']],
            ['Middle Name: ', '', ['middle_name']],
            ['  Last Name: ', '', ['last_name']],
            ['     Rating: ', '0', ['initial_rating', 'rating']],
            ['  Dues owed:$', '', ['dues']],
            ['   K Factor: ', '1.0', ['kfactor']]
            ]

        self.cursor_location = [0, 0]

    def display(self):
        return [field[0] + field[1] for field in self.fields]

    def handle_key(self, key):
        if key in [curses.KEY_ENTER, 10, 13]:
            self.cursor_location[1] += 1
            if self.cursor_location[1] == len(self.fields):
                # Apply changes
                return self.return_constructor(self.database)

        elif key in [curses.KEY_DOWN, 9]:
            self.cursor_location[1] += 1
        elif key == curses.KEY_UP:
            self.cursor_location[1] -= 1
        elif key == curses.KEY_LEFT:
            self.cursor_location[0] -= 1
        elif key == curses.KEY_RIGHT:
            self.cursor_location[0] += 1
        elif key in [curses.KEY_BACKSPACE, 127]:
            if self.cursor_location[0]:
                self.cursor_location[0] -= 1
                to_pop = self.cursor_location[0]
                string_to_change = self.fields[self.cursor_location[1]][1]
                self.fields[self.cursor_location[1]][1] = string_to_change[:to_pop] + string_to_change[to_pop + 1:]
        else:
            to_pop = self.cursor_location[0]
            string_to_change = self.fields[self.cursor_location[1]][1]
            self.fields[self.cursor_location[1]][1] = string_to_change[:to_pop] + chr(key) + string_to_change[to_pop:]
            self.cursor_location[0] += 1

        self.cursor_location[1] = sorted([0, self.cursor_location[1], len(self.fields) - 1])[1]
        self.cursor_location[0] = sorted([0, self.cursor_location[0], len(self.fields[self.cursor_location[1]][1])])[1]

        return self

    def cursor_position(self):
        return self.cursor_location[0] + len(self.fields[self.cursor_location[1]][0]), self.cursor_location[1]
