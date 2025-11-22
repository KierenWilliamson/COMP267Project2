import os
import mysql.connector
from flask import Flask, jsonify
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

@app.get("/tables")
def get_tables():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        db.close()

        return jsonify({"tables": tables})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    # This line must run before Tkinter can send requests
    app.run(debug=True)
