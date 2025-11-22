from flask import Blueprint, jsonify
from api import database

bp = Blueprint('routes', __name__)

# GET all tables
@bp.route("/tables", methods=["GET"])
def get_tables():
    '''
    Get all tables in the database.
    '''
    try:
        db = database.init_db()
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()

        return jsonify({"tables": tables})
    except Exception as e:
        return jsonify({"error": str(e)})

# GET all gov websites
@bp.route("/websites", methods=["GET"])
def get_websites():
    '''
    Get all government websites
    '''
    try:
        db = database.init_db()
        cursor = db.cursor()
        cursor.execute("SELECT url FROM gov_website")
        result = cursor.fetchall()
        website_list = list()
        for row in result:
            website_list.append(row[0])
        return jsonify({"urls": website_list})
    except Exception as e:
        return jsonify({"error": str(e)})

bp.route("/tables/<table_name>", methods=["POST"])
def create_data():

