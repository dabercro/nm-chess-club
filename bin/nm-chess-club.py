#! /usr/bin/env python3

import sys
import curses

from nm_chess_club import main

if __name__ == '__main__':
    curses.wrapper(
        main.main,
        filename=sys.argv[1] if len(sys.argv) > 1 else None
    )
