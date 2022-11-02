import curses

from .text_buffers_state import TextBuffersState

from ..sql_edit import update_table

class AddPlayerState(TextBuffersState):
    def __init__(self, database, return_constructor):
        super().__init__(database, return_constructor)

        self.fields = [
            [' First Name: ', '', ['first_name'], str],
            ['Middle Name: ', '', ['middle_name'], str],
            ['  Last Name: ', '', ['last_name'], str],
            ['     Rating: ', '', ['initial_rating', 'rating'], int],
            ['  Dues owed:$', '', ['dues'], int],
            ['   K Factor: ', '1.0', ['kfactor'], float]
            ]

    def update(self):
        update_table(self.database.get_cursor(), "INSERT", "players", self.key_value_pairs())
