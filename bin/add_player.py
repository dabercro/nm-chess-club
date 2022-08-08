#! /usr/bin/env python3

from nm_chess_club import sql_edit

if __name__ == '__main__':
    if not sql_edit.get_module().exists():
        sql_edit.create_database()
    else:
        print('Already exists')
