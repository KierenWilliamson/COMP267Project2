from api.db_api import app

if __name__ == "__main__":
    # This line must run before Tkinter can send requests
    app.run(debug=True)