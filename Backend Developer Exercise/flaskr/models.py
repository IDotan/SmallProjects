import sqlite3

DATABASE = 'url.db'


def create_db():
    """
    | create the url.db when the db don't exists yet
    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS url
    (id INTEGER PRIMARY KEY,
    long_url VARCHAR(100),
    short_url VARCHAR(100),
    clicks INTEGER )""")
    connection.commit()
    connection.close()
