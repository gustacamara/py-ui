import sqlite3
cursor = None

def create_db():
    global cursor
    db = sqlite3.connect('database/pyui.db')
    cursor = db.cursor()
    return db,cursor


def get_query(query):
    cursor.execute(query)
    return cursor.fetchall()
