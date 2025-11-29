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


@bp.route("/tables/<table_name>", methods=["GET"])
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
@bp.route("/tables/<table_name>", methods=["PUT"])
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
        db = database.get_fresh_connection()
        cursor = db.cursor()

        data = request.get_json()

        columns = data.get("columns")   # list
        values  = data.get("values")    # list
        where   = data.get("where")     # dict ex: {"id": 5}

        # Validate
        if not columns or not values or not where:
            return jsonify({"error": "Missing data"}), 400

        if len(columns) != len(values):
            return jsonify({"error": "Columns and values length mismatch"}), 400

        # Build SET clause
        set_clause = ", ".join([f"{col} = %s" for col in columns])

        # Build WHERE clause safely
        where_cols = list(where.keys())
        where_vals = list(where.values())

        where_clause = " AND ".join([f"{col} = %s" for col in where_cols])

        sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};"

        params = values + where_vals

        cursor.execute(sql, params)
        db.commit()

        rows = cursor.rowcount
        cursor.close()
        db.close()

        return jsonify({"message": f"{rows} rows updated successfully"})
    except Exception as e:
        return jsonify({"error" : str(e)})

    
# delete row from table
# IN: table name, WHERE condition
# OUT: void
@bp.route("/tables/<table_name>", methods=["DELETE"])
def delete_row(table_name):
    '''
    Performs the operation:\n
    DELETE FROM (Table) WHERE (condition)\n
    DELETE /tables/<table>\n
    JSON: { "where": { "col": value } }
    '''
    try:
        data = request.get_json()
        where = data.get("where")

        if not where or not isinstance(where, dict):
            return jsonify({"error": "'where' must be an object"}), 400

        db = database.get_fresh_connection()
        cursor = db.cursor()

        # Validate columns
        cursor.execute(f"DESCRIBE {table_name}")
        valid_cols = [col[0] for col in cursor.fetchall()]

        for col in where.keys():
            if col not in valid_cols:
                return jsonify({"error": f"Invalid column in WHERE: {col}"}), 400

        # Build WHERE clause
        where_clause = " AND ".join([f"{col} = %s" for col in where])
        where_vals = list(where.values())

        sql = f"DELETE FROM {table_name} WHERE {where_clause};"
        cursor.execute(sql, where_vals)
        db.commit()

        rows = cursor.rowcount
        cursor.close()
        db.close()

        return jsonify({"deleted": rows}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# create count endpoint
# IN: table name, column name
# OUT: returns the record count associated with the specified column
@bp.route("/tables/<table_name>/count/<column_name>", methods=["GET"])
def count_column(table_name, column_name):
    '''
    call to this endpoint should look like this:\n
    GET /tables/<table>/count/<column>
    '''
    try:
        db = database.get_fresh_connection()
        cursor = db.cursor()

        # Validate column exists
        cursor.execute(f"DESCRIBE {table_name}")
        valid_cols = [col[0] for col in cursor.fetchall()]

        if column_name not in valid_cols:
            return jsonify({"error": f"Invalid column: {column_name}"}), 400
        
        sql = f"SELECT COUNT({column_name}) FROM {table_name};"
        cursor.execute(sql)
        count = cursor.fetchone()[0]

        cursor.close()
        db.close()

        return jsonify({"count": count}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# create view table
# IN: view name, columns, table name
# OUT: void
@bp.route("/views", methods=["POST"])
def create_view():
    '''
    Call to this endpoint should look like this:\n
    POST /views\n
    JSON: { "view": "...", "table": "...", "columns": ["a","b"] }

    '''
    try:
        data = request.get_json()

        view_name = data.get("view")
        table_name = data.get("table")
        columns = data.get("columns", [])

        if not view_name or not table_name or not columns:
            return jsonify({"error": "Missing view, table, or columns"}), 400
        
        db = database.get_fresh_connection()
        cursor = db.cursor()

        # Validate column names
        cursor.execute(f"DESCRIBE {table_name}")
        valid_cols = [col[0] for col in cursor.fetchall()]

        for col in columns:
            if col not in valid_cols:
                return jsonify({"error": f"Column '{col}' does not exist"}), 400

        col_list = ", ".join(columns)

        sql = f"CREATE VIEW {view_name} AS SELECT {col_list} FROM {table_name};"
        cursor.execute(sql)
        db.commit()

        cursor.close()
        db.close()

        return jsonify({"message": f"View '{view_name}' created"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

