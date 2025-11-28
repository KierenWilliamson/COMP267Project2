from flask import Blueprint, jsonify, request
from api import database

bp = Blueprint('routes', __name__)


# GET all tables
@bp.route("/tables", methods=["GET"])
def get_tables():
    '''
    Get all tables in the database.\n
    GET/tables
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
    Get all government websites.\n
    GET/websites
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


@bp.route("/tables/<table_name>", methods=["POST"])
def insert_into_table(table_name):
    try:
        db = database.init_db()
        cursor = db.cursor()

        data = request.get_json()

        columns = data.get("columns")
        rows = data.get("rows")  # list of lists

        if not columns or not rows:
            return jsonify({"error": "Missing 'columns' or 'rows'"}), 400

        # Get real table columns
        cursor.execute(f"DESCRIBE {table_name}")
        # FIX: Remove extra curly braces
        valid_columns = [col[0] for col in cursor.fetchall()]

        # Ensure client-sent columns exist
        for col in columns:
            if col not in valid_columns:
                return jsonify({"error": f"Invalid column name: {col}"}), 400

        # Build SQL safely
        column_list = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))

        sql = f"INSERT IGNORE INTO {table_name} ({column_list}) VALUES ({placeholders})"

        # FIX: Use the same cursor for executemany
        cursor.executemany(sql, rows)

        # FIX: Get rowcount before closing cursor
        rows_inserted = cursor.rowcount

        db.commit()
        cursor.close()

        return jsonify({"message": f"{rows_inserted} rows inserted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/select/<table_name>", methods=["GET"])
def select_table(table_name):
    '''
    Performs the operation:\n
    SELECT(expression){Table}
    '''
    try:
        # Get a fresh connection to ensure we read the latest data
        db = database.get_fresh_connection()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        tables = cursor.fetchall()
        cursor.close()
        db.close()  # Close the fresh connection
        return jsonify({"selected_tables": tables})
    except Exception as e:
        return jsonify({"error": str(e)}), 500