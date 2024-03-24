import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

class DB:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls, *args, *kwargs)
            cls._instance.connection = None
        return cls._instance
    
    def connect(self):
        db_file = 'databases/'+os.getenv("DB_NAME")
        if not db_file:
            print('Error: Database file not specified in environment variables.')
            return None
        
        if not self.connection:
            try:
                self.connection = sqlite3.connect(db_file)
                print(f"Connected to sqlite database: {db_file}")
            except sqlite3.Error as e:
                print("Error connecting to sqlite database:", e)
        
        return self.connection 
                
    def execute_query(self, query, parameters=None):
        try:
            cursor = self.connection.cursor()
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            result = cursor.fetchall()  
                      
            return result
        except sqlite3.Error as e:
            self.connection.rollback()
            print("Error executing query:", e)
            
    def execute_insert_query(self, query, parameters=None):
        try:
            cursor = self.connection.cursor()
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
                      
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            self.connection.rollback()
            print("Error executing query:", e)
            
    def execute_transaction(self, queries):
        try:
            cursor = self.connection.cursor()
            for query, parameters in queries:
                cursor.execute(query, parameters)
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            print("Transaction failed and rolled back:", e)
        finally:
            self.connection.close()
                
def create_table(conn):
    create_table_query ="""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            slug VARCHAR(255) NOT NULL,
            start_date DATETIME NOT NULL,
            end_date DATETIME NOT NULL
        )
    """
    conn.execute_query(create_table_query)
    
if __name__ == '__main__':
     connection = DB()
     connection.connect()
     
     create_table(connection)
        