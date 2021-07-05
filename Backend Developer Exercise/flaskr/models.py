import sqlite3


def create_db(database):
    """
    | create the url.db when the db don't exists yet
    """
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS url
    (id INTEGER PRIMARY KEY,
    long_url VARCHAR(100),
    short_url VARCHAR(100),
    clicks INTEGER )""")
    connection.commit()
    connection.close()
