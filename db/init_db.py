import sqlite3

def initialize_database():
    try:
        # this throws an exception in the database does not exist
        conn = sqlite3.connect('file:songs.db?mode=rw', uri=True)
    except:
        connection = sqlite3.connect('songs.db')

        with open('db/schema.sql') as schema_script:
            connection.executescript(schema_script.read())

        with open('db/seed_data.sql') as seed_script:
            connection.executescript(seed_script.read())

        connection.commit()
        connection.close()