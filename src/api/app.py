from flask import Flask
from . import database
from . import routes

# load .env file
app = Flask(__name__)

# def get_db():
#     app.config['MYSQL_DB'] = os.getenv("DB_NAME")
#     app.config['MYSQL_USER'] = os.getenv("DB_USER")
#     app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
#     app.config['MYSQL_HOST'] = os.getenv("DB_HOST")

@app.teardown_appcontext
def cleanup(error):
    database.close_db()

# Register routes from the routes file
app.register_blueprint(routes.bp)


if __name__ == "__main__":
    # This line must run before Tkinter can send requests
    app.run(debug=True)
