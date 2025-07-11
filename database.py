import sqlite3
from sqlite3 import Error
import os

def create_connection():
       db_path = os.path.join(os.path.dirname(__file__), "todo.db")
       conn = None
       try:
           conn = sqlite3.connect(db_path)
           return conn
       except Error as e:
           print(f"Error connecting to database: {e}")
       return conn

def create_table():
       conn = create_connection()
       try:
           cursor = conn.cursor()
           cursor.execute('''
               CREATE TABLE IF NOT EXISTS tasks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   description TEXT,
                   priority TEXT DEFAULT 'Medium',
                   completed BOOLEAN DEFAULT 0,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               )
           ''')
           conn.commit()
       except Error as e:
           print(f"Error creating table: {e}")
       finally:
           conn.close()