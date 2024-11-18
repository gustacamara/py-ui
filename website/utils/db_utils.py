import sqlite3
import json

db = None

def create_db(recreate=False):
    global db
    db = sqlite3.connect('database/pyui.db', check_same_thread=False)
    cursor = db.cursor()

    if recreate:
        drop_tables_sql = """
        DROP TABLE IF EXISTS cabs;
        DROP TABLE IF EXISTS composition;
        DROP TABLE IF EXISTS sensor;
        DROP TABLE IF EXISTS turnout;
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS wagon;
        DROP TABLE IF EXISTS credentials;
        """
        cursor.executescript(drop_tables_sql)

        create_tables_sql = """
        CREATE TABLE IF NOT EXISTS cabs (
            id INTEGER UNIQUE,
            manufacturer TEXT,
            model TEXT,
            PRIMARY KEY(id)
        );

        CREATE TABLE IF NOT EXISTS sensor (
            id INTEGER UNIQUE,
            location TEXT,
            type INTEGER,
            PRIMARY KEY(id)
        );

        CREATE TABLE IF NOT EXISTS turnout (
            id INTEGER UNIQUE,
            actuator TEXT,
            left_angle INTEGER,
            right_angle INTEGER,
            PRIMARY KEY(id)
        );

        CREATE TABLE IF NOT EXISTS users (
            username TEXT UNIQUE,
            password TEXT,
            PRIMARY KEY(username)
        );
        """

        cursor.executescript(create_tables_sql)
        start_query("INSERT INTO users (username, password) VALUES ('admin', 'admin')") # Create admin user
        start_query("INSERT INTO users (username, password) VALUES ('user', 'user')") # Create admin user
        start_query("INSERT INTO cabs (id, manufacturer, model) VALUES (1, 'Frateschi', 'U20')")
        start_query("INSERT INTO sensor (id, location, type) VALUES (1, 'Restaurante 8Bits', 'RFID')")
        start_query("INSERT INTO sensor (id, location, type) VALUES (2, 'Poço das capivaras', 'Infravermelho')")
        start_query("INSERT INTO turnout (id, left_angle, right_angle) VALUES (1, 0, 60)")
        start_query("INSERT INTO turnout (id, left_angle, right_angle) VALUES (2, 60, 0)")
        db.commit()

    cursor.close()
    return db


def start_query(query):
    global db
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    result = cursor.fetchall()
    cursor.close()
    return result
