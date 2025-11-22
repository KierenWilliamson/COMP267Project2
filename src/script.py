import os
import tkinter.messagebox as tkmb
from tkinter import Menu
import customtkinter as ctk
from api.app import app as api_app

# Windows
app = ctk.CTk()
app.geometry("400x400")
app.title("Government Website Database Landing")
app.attributes("-topmost", 1)
app.attributes("-fullscreen", True)

# sanple API request
with api_app.test_client() as client:
    response = client.post("/tables/gov_website",json={"columns": ["name", "url"],"rows": [["Test site", "https://example.com"],["Another site", "https://xyz.com"]]})
    print(response.get_json())


# COMMANDS / FUNCTIONS
def login():
    '''
    Accepts or rejects the user's login attempt based on the values
    set in the environment variables file
    '''
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if user_entry.get() == username and user_pass.get() == password:
        tkmb.showinfo(title="Login Successful", message="You have logged in Successfully")
        app.withdraw()
        create_dashboard()
    elif user_entry.get() == username and user_pass.get() != password:
        tkmb.showwarning(title='Wrong password',
             message='Please check your password')
    elif user_entry.get() != username and user_pass.get() == password:
        tkmb.showwarning(title='Wrong username',
             message='Please check your username')
    else:
        tkmb.showerror(title="Login Failed",
           message="Invalid Username and password")

def create_dashboard():
    '''
    Creates the dashboard window
    '''
    dashboard_window = ctk.CTkToplevel(app)
    dashboard_window.title("Government Website Database")
    dashboard_window.attributes("-fullscreen", True)
    dashboard_window.columnconfigure(0, weight=1)
    dashboard_window.columnconfigure(1, weight=1)
    dashboard_window.columnconfigure(2, weight=1)
    dashboard_frame = ctk.CTkFrame(dashboard_window)
    dashboard_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    for row in range(2):
        dashboard_frame.grid_rowconfigure(row, weight=1)

    for col in range(3):
        dashboard_frame.grid_columnconfigure(col, weight=1)

    dash_option_menu = Menu(dashboard_window)
    dashboard_window.config(menu=dash_option_menu)

    dash_file_menu = Menu(dash_option_menu,tearoff=0)
    dash_file_menu.add_command(label="Exit", command=dashboard_window.destroy)
    dash_file_menu.add_separator()
    dash_option_menu.add_cascade(label="File", menu=dash_file_menu)

    create_button = ctk.CTkButton(dashboard_frame,text="CREATE", command=lambda: [dashboard_window.withdraw(), insert_data()])
    create_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    read_button = ctk.CTkButton(dashboard_frame, text="READ")
    read_button.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
    update_button = ctk.CTkButton(dashboard_frame, text="UPDATE")
    update_button.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")
    delete_button = ctk.CTkButton(dashboard_frame, text="DELETE")
    delete_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
    report_button = ctk.CTkButton(dashboard_frame, text="GENERATE REPORTS")
    report_button.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
    website_button = ctk.CTkButton(dashboard_frame, text="LIST WEBSITES")
    website_button.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

def insert_data():
    '''
    Create a new window and insert data
    '''
    create_window = ctk.CTkToplevel(app)
    create_window.title("Insert into Database")
    create_window.attributes("-fullscreen", True)

# WIDGETS
# Login Window
heading_label = ctk.CTkLabel(app,text="Welcome to the Government Website Database")
heading_label.pack(pady=20)
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20,padx=40,fill='both',expand=True)
login_label = ctk.CTkLabel(master=frame,text='MASU - Modern Authentication System UI')
login_label.pack(pady=12,padx=10)

user_entry= ctk.CTkEntry(master=frame,placeholder_text="Username")
user_entry.pack(pady=12,padx=10)
user_pass= ctk.CTkEntry(master=frame,placeholder_text="Password",show="*")
user_pass.pack(pady=12,padx=10)

login_button = ctk.CTkButton(master=frame,text='Login', command=login)
login_button.pack(pady=12,padx=10)

# Menu Bar
option_menu = Menu(app)
app.config(menu=option_menu)

file_menu = Menu(option_menu,tearoff=0)

file_menu.add_command(label="Exit", command=app.destroy)
file_menu.add_separator()
option_menu.add_cascade(label="File", menu=file_menu)

# main event loop, must be at EOF
app.mainloop()
