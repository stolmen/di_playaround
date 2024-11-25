import sqlite3


def create_db_client(db_filename):
    return sqlite3.connect(db_filename)
