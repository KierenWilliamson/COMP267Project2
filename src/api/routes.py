from flask import Blueprint, jsonify
from api import database

bp = Blueprint('routes', __name__)

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
