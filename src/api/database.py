import os
import pymysql
from dotenv import load_dotenv

DB = None
load_dotenv()

def init_db():
    '''
    Initialize the database connection to the MySQL
    database using the environment variables.
    '''
    global DB
    if DB is None or not DB.open:
        DB = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME"),
            autocommit=False,  # Explicit control over commits
            cursorclass=pymysql.cursors.Cursor
        )
    return DB

def get_fresh_connection():
    '''
    Get a fresh database connection.
    This ensures you're not reading the initial data.
    '''
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        autocommit=False,
        cursorclass=pymysql.cursors.Cursor
    )

def close_db():
    '''
    Close the MySQL database connection.
    '''
    global DB
    if DB is not None:
        DB.close()
        DB = None
