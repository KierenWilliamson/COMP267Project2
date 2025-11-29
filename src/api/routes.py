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


# FIXME: change route to /tables/<table_name>
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
        return jsonify({"error" : str(e)})

# update table endpoint
# IN: Table name, column names, and new data values, and Where condition
# OUT: void
@bp.route("/tables/<table_name>", method=["PUT"])
def update_table(table_name):
    '''
    Performs the operation:\n
    UPDATE (Table)\n
    SET column1 = value1, column2 = . . .\n
    WHERE (condition)\n
    \n
    input data should be in the form of:\n
    json={"columns": ["column1", "column2", . . .], "values": ["value1", "value2", . . .], "where": "condition"}
    '''
    try:
        db = database.init_db()
        cursor = db.cursor()

        data = request.get_json()

        columns = data.get("columns") #list
        values = data.get("values")  #list
        where_condition = data.get("where") #string

        if not columns or not values or not where_condition:
            return jsonify({"error": "Missing 'columns' or 'rows' or 'where' condition"}), 400

        # Get real table columns
        cursor.execute(f"DESCRIBE {table_name}")
        # table_info = cursor.fetchall()
        valid_columns = [col[0] for col in cursor.fetchall()]
        cursor.close()

        # Ensure client-sent columns exist
        for col in columns:
            if col not in valid_columns:
                return jsonify({"error": f"Invalid column name: {col}"}), 400
        
        # Ensure each column has an associated value
        if len(columns) != len(values):
            return jsonify({"error":
                f"Disproportionate number of columns to values, {columns} columns and {values} values"}), 400

        # Build SQL safely
        set_list = ""
        for i in range(len(columns)):
            if i == len(columns) -1:
                set_list += f"{columns[i]} = {values[i]}"
            set_list += f"{columns[i]} = {values[i]},"

        sql = f"UPDATE {table_name} SET {set_list} WHERE {where_condition};"

        db.cursor().execute(sql)
        db.commit()

        return jsonify({"message": f"{cursor.rowcount} rows updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
# delete row from table
# IN: table name, WHERE condition
# OUT: void
#
# create count endpoint
# IN: table name, column name
# OUT: returns the record count associated with teh specified column
# 
# create view table
# IN: view name, columns, table name
# OUT: void
