import api.database as database
import api.routes as routes
from flask import Flask

# load .env file
flask_app = Flask(__name__)

@flask_app.teardown_appcontext
def cleanup(error):
    database.close_db()

# Register routes from the routes file
flask_app.register_blueprint(routes.bp)


if __name__ == "__main__":
    # This line must run before Tkinter can send requests
    flask_app.run(debug=True)
