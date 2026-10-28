import sqlite3
import os

BASE_DIR=os.path.abspath(
    os.path.dirname()
)

DB_PATH=os.path.join("data","documents.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():

    #Create connection btw databases
    conn=get_connection()
    cursor=conn.cursor()

    #Create Tables 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        Path TEXT,
        thumbnail_path TEXT,
        description TEXT,
        upload_date TEXT,
        Total_Pages INTEGER)
    """)

    #Commit and release the connection
    conn.commit()
    conn.close()

