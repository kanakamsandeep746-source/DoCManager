import sqlite3
import os
import sys
#common path config
BASE_DIR=os.path.abspath(
    os.path.join(os.path.dirname(__file__),'..')
)
sys.path.append(BASE_DIR)

DB_PATH=os.path.join(BASE_DIR,"data","documents.db")
#connection code
def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():

    #Create connection btw databases
    connection=get_connection()
    cursor=connection.cursor()

    #Create Tables 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        Path TEXT,
        thumbnail_path TEXT,
        tags TEXT,
        description TEXT,
        upload_date TEXT,
        Total_Pages INTEGER)
    """)
    # cursor.execute("PRAGMA table_info(documents)")
    # print(cursor.fetchall())
    #Comm it and release the connections

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS page_vists(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        page_number INTEGER,
        time_stamp TEXT
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS app_visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        timestamp TEXT
    )
    """)
    connection.commit()
    connection.close()

