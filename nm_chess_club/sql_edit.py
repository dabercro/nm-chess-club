
def create_database(cursor):
    """
    Creates new database if the old one doesn't exist
    """
    # dues are stored in cents
    cursor.executescript(
"""
CREATE TABLE players(
  first_name VARCHAR (64) NOT NULL,
  middle_name VARCHAR (64),
  last_name VARCHAR (64) NOT NULL,
  initial_rating INTEGER NOT NULL,
  dues INTEGER NOT NULL,
  rating INTEGER NOT NULL,
  kfactor REAL NOT NULL,
  UNIQUE(first_name, middle_name, last_name)
);

CREATE TABLE match(
  date DATE NOT NULL,
  round INTEGER NOT NULL,
  status INTEGER NOT NULL,
  FOREIGN KEY(status) REFERENCES statuses(rowid)
);

CREATE TABLE statuses(
  status VARCHAR(16) NOT NULL UNIQUE
);

CREATE TABLE incomplete(
  match INTEGER NOT NULL UNIQUE,
  black_player INTEGER NOT NULL,
  white_player INTEGER NOT NULL,
  FOREIGN KEY(match) REFERENCES match(rowid),
  FOREIGN KEY(black_player) REFERENCES players(rowid),
  FOREIGN KEY(white_player) REFERENCES players(rowid)
);

CREATE TABLE results(
  player INTEGER NOT NULL,
  color INTEGER NOT NULL,
  match INTEGER NOT NULL,
  SCORE REAL NOT NULL,
  rating_before INTEGER NOT NULL,
  rating_after INTEGER NOT NULL,
  k_factor REAL NOT NULL,
  FOREIGN KEY(player) REFERENCES players(rowid)
  FOREIGN KEY(color) REFERENCES colors(rowid)
  FOREIGN KEY(match) REFERENCES match(rowid)
);

CREATE TABLE colors(
  color VARCHAR(6) NOT NULL UNIQUE
);
""")

    cursor.executemany("INSERT INTO statuses (status) VALUES (?)",
                       [(status ,) for status in
                        ['In Progress', 'Completed', 'Canceled']])

    cursor.executemany("INSERT INTO colors (color) VALUES (?)",
                       [(color ,) for color in
                        ['Black', 'White']])
