import sqlite3
from sqlite3 import Connection

from data.config import DB_FILE


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = dict_factory
        print(f"Connected to SQLite database version: {sqlite3.version}")
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn.cursor()


database_connection: Connection = create_connection(DB_FILE)
