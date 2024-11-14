import sqlite3

def create_db(recreate=False):
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
        """
        cursor.executescript(drop_tables_sql)
        
        create_tables_sql = """
        CREATE TABLE IF NOT EXISTS cabs (
            id INTEGER UNIQUE,
            manufacturer TEXT,
            model TEXT,
            image TEXT,
            level_capacity INTEGER,
            downhill_capacity INTEGER,
            slope_capacity INTEGER,
            PRIMARY KEY(id)
        );

        CREATE TABLE IF NOT EXISTS composition (
            id INTEGER UNIQUE,
            wagon_id INTEGER,
            cab_id INTEGER,
            description TEXT,
            PRIMARY KEY(id)
        );

        CREATE TABLE IF NOT EXISTS sensor (
            id INTEGER UNIQUE,
            sensor TEXT,
            value INTEGER,
            PRIMARY KEY(id)
        );

        CREATE TABLE IF NOT EXISTS turnout (
            id INTEGER UNIQUE,
            actuator TEXT,
            value INTEGER,
            PRIMARY KEY(id)
        );

        CREATE TABLE IF NOT EXISTS users (
            username TEXT UNIQUE,
            password TEXT,
            PRIMARY KEY(username)
        );

        CREATE TABLE IF NOT EXISTS wagon (
            id INTEGER UNIQUE,
            description TEXT,
            image TEXT,
            manufacturer TEXT,
            model TEXT,
            PRIMARY KEY(id)
        );
        """
        
        cursor.executescript(create_tables_sql)
        start_query(db, "INSERT INTO users (username, password) VALUES ('admin', 'admin')") # Create admin user
        start_query(db, "INSERT INTO users (username, password) VALUES ('user', 'user')") # Create admin user
        db.commit()

    cursor.close()
    return db


def start_query(db, query):
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    result = cursor.fetchall()
    cursor.close()
    return result
