import sqlite3
from db.db import DB

def execute_migration(connection, migration_script):
    try:
        cursor = connection.cursor()
        cursor.executescript(migration_script)
        connection.commit()
        print("Migration executed successfully.")
    except sqlite3.Error as e:
        print("Error executing migration:", e)
        connection.rollback()

def migrate_database():
    # Connect to the SQLite database
    connection = DB().connect()
    if not connection:
        return
    
    create_table_query ="""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            slug VARCHAR(255) NOT NULL,
            start_date DATETIME NOT NULL,
            end_date DATETIME NOT NULL
        )
    """
    execute_migration(connection, create_table_query)
    
    # Close the connection
    connection.close()






