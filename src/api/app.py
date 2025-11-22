from flask import Flask
from . import database
from . import routes

# load .env file
app = Flask(__name__)

@app.teardown_appcontext
def cleanup(error):
    database.close_db()

# Register routes from the routes file
app.register_blueprint(routes.bp)


if __name__ == "__main__":
    # This line must run before Tkinter can send requests
    app.run(debug=True)
