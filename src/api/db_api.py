import mysql.connector
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# load .env file
load_dotenv()
app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
