import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db.sqlite')


# connecting to the database
# if database is not exist, it creates
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()


try:
    # creating the collections table
    c.execute("CREATE TABLE COLLECTIONS (TEST TEXT)")
    conn.commit()
    conn.close()
except:
    pass
