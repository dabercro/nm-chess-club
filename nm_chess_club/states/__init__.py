class State(object):
    """
    Specifies functions needed by all states.
    Other states should inherit from this class,
    and reimplment functions that would otherwise throw.
    """
    def __init__(self, database, return_constructor=None):
        self.database = database
        self.return_constructor = return_constructor

    def display(self):
        raise NotImplementedError

    def handle_key(self, key):
        raise NotImplementedError

    def cursor_position(self):
        raise NotImplementedError

    def running(self):
        return True
