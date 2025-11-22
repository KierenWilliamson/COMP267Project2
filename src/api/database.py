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
    if DB is None:
        DB = pymysql.connect(host=os.getenv("DB_HOST"),
                           user=os.getenv("DB_USER"),
                           password=os.getenv("DB_PASSWORD"),
                           db=os.getenv("DB_NAME"))
        return DB

def close_db():
    '''
    Close the MySQL database connection.
    '''
    global DB
    if DB is not None:
        DB.close()
        DB = None
