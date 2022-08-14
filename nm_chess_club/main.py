import curses

from . import sqlite3_database
from . import sql_edit
from .states import start

TOP_MARGIN = 2
LEFT_MARGIN = 2

def main(stdscr, **connection_params):

    curses.start_color()
    curses.use_default_colors()

    database = sqlite3_database.DataBase(connection_params)

    if not database.exists():
        sql_edit.create_database(database.get_cursor())

    state = start.StartState(database)

    max_y, max_x = stdscr.getmaxyx()

    while state.running():
        # Display the state text
        text = state.display()
        cursor_x, cursor_y = state.cursor_position()

        stdscr.clear()

        stdscr.addstr('\n' * TOP_MARGIN)

        for line in text:
            stdscr.addstr(' ' * LEFT_MARGIN + line + '\n')

        stdscr.move(cursor_y + TOP_MARGIN, cursor_x + LEFT_MARGIN)

        stdscr.refresh()

        key = stdscr.getch()

        if key == 27:
            break

        state = state.handle_key(key)
