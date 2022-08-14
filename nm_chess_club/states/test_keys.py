from . import State

class TestKeysState(State):
    def __init__(self, database, return_constructor):
        super().__init__(database, return_constructor)

        self.keys = []

    def display(self):
        return self.keys

    def handle_key(self, key):
        self.keys.append(str(key))
        return self

    def cursor_position(self):
        return 0, len(self.keys)
