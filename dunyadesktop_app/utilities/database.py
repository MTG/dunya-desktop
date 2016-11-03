import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db.sqlite')


def connect():
    # connecting to the database
    # if database is not exist, it creates
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    return conn, c


def add_collection(conn, c, list_name):
    try:
        # creating the collections table
        c.execute("CREATE TABLE {tn} (DOCID TEXT)".format(tn=list_name))
        conn.commit()
        conn.close()
        print(list_name, 'added')
    except:
        pass
