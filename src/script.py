import os
import tkinter.messagebox as tkmb
from tkinter import Menu
import customtkinter as ctk
from api.app import flask_app as api_app
from api import database

app = ctk.CTk()
app.geometry("1200x800")
app.title("Government Website Database Landing")
app.attributes("-topmost", 1)
# Center the window on screen
app.update_idletasks()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - 1200) // 2
y = (screen_height - 800) // 2
app.geometry(f"1200x800+{x}+{y}")

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
    dashboard_window.geometry("1200x800")
    # Center the window
    dashboard_window.update_idletasks()
    screen_width = dashboard_window.winfo_screenwidth()
    screen_height = dashboard_window.winfo_screenheight()
    x = (screen_width - 1200) // 2
    y = (screen_height - 800) // 2
    dashboard_window.geometry(f"1200x800+{x}+{y}")
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

    dash_file_menu = Menu(dash_option_menu, tearoff=0)
    dash_file_menu.add_command(label="Exit", command=dashboard_window.destroy)
    dash_file_menu.add_separator()
    dash_option_menu.add_cascade(label="File", menu=dash_file_menu)

    create_button = ctk.CTkButton(dashboard_frame, text="CREATE",
                                  command=lambda: [dashboard_window.withdraw(), insert_data(dashboard_window)])
    create_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    read_button = ctk.CTkButton(dashboard_frame, text="READ",
                                command=lambda: [dashboard_window.withdraw(), read_data(dashboard_window)])
    read_button.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
    update_button = ctk.CTkButton(dashboard_frame, text="UPDATE",
                                  command=lambda: [dashboard_window.withdraw(), update_data(dashboard_window)])
    update_button.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")
    delete_button = ctk.CTkButton(dashboard_frame, text="DELETE",
                                  command=lambda: [dashboard_window.withdraw(), delete_data(dashboard_window)])
    delete_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
    report_button = ctk.CTkButton(dashboard_frame, text="GENERATE REPORTS",
                                  command=lambda: [dashboard_window.withdraw(), generate_reports(dashboard_window)])
    report_button.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
    website_button = ctk.CTkButton(dashboard_frame, text="LIST WEBSITES",
                                   command=lambda: [dashboard_window.withdraw(), list_websites(dashboard_window)])
    website_button.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")


def insert_data(dashboard_window):
    '''
    Create a new window and insert data with input fields for each column
    '''
    create_window = ctk.CTkToplevel(app)
    create_window.title("Insert into Database")
    create_window.geometry("1200x800")
    # Center the window
    create_window.update_idletasks()
    screen_width = create_window.winfo_screenwidth()
    screen_height = create_window.winfo_screenheight()
    x = (screen_width - 1200) // 2
    y = (screen_height - 800) // 2
    create_window.geometry(f"1200x800+{x}+{y}")

    # Frames inside the create window
    top_frame = ctk.CTkFrame(master=create_window)
    top_frame.pack(fill="x", pady=10, padx=10)
    middle_frame = ctk.CTkFrame(master=create_window)
    middle_frame.pack(fill="both", expand=True, pady=10, padx=10)
    bottom_frame = ctk.CTkFrame(master=create_window)
    bottom_frame.pack(fill="x", pady=10, padx=10)

    # Exit button
    exit_button = ctk.CTkButton(
        master=top_frame,
        text="← Back to Dashboard",
        command=lambda: [create_window.destroy(), dashboard_window.deiconify()],
        fg_color="gray",
        hover_color="darkgray"
    )
    exit_button.pack(side="left", padx=10, pady=10)

    # Dictionary of tables with associated columns
    tables = {
        "department": [
            "department_id",
            "name",
            "description"
        ],
        "district": [
            "district_id",
            "name",
            "description"
        ],
        "topic": [
            "topic_id",
            "name",
            "description"
        ],
        "gov_website": [
            "website_id",
            "name",
            "url",
            "department_id",
            "district_id",
            "topic_id"
        ]
    }

    selected_table = ctk.StringVar(value="Select a table")

    table_label = ctk.CTkLabel(master=top_frame, text="Select Table:", font=("Arial", 14, "bold"))
    table_label.pack(side="left", padx=10)

    table_dropdown = ctk.CTkComboBox(
        master=top_frame,
        values=list(tables.keys()),
        variable=selected_table,
        width=300,
        command=lambda _=None: show_input_fields()
    )
    table_dropdown.pack(side="left", pady=10)

    input_fields = {}

    def show_input_fields():
        # Clear previous widgets
        for widget in middle_frame.winfo_children():
            widget.destroy()
        for widget in bottom_frame.winfo_children():
            widget.destroy()

        table = selected_table.get()
        input_fields.clear()

        # Create a scrollable frame for input fields
        scroll_frame = ctk.CTkScrollableFrame(master=middle_frame, width=600, height=400)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        title_label = ctk.CTkLabel(
            master=scroll_frame,
            text=f"Enter data for {table}:",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Create input fields for each column
        for col in tables.get(table, []):
            field_frame = ctk.CTkFrame(master=scroll_frame)
            field_frame.pack(pady=5, padx=10, fill="x")

            label = ctk.CTkLabel(master=field_frame, text=f"{col}:", width=150, anchor="w")
            label.pack(side="left", padx=5)

            entry = ctk.CTkEntry(master=field_frame, width=400, placeholder_text=f"Enter {col}")
            entry.pack(side="left", padx=5)

            input_fields[col] = entry

        # Submit button
        submit_btn = ctk.CTkButton(
            master=bottom_frame,
            text="Insert Data",
            command=submit_data,
            fg_color="green",
            hover_color="darkgreen"
        )
        submit_btn.pack(pady=10)

    def submit_data():
        table = selected_table.get()
        if table == "Select a table":
            tkmb.showerror("Error", "Please select a table")
            return

        # Collect data from input fields
        columns = []
        values = []

        for col, entry in input_fields.items():
            value = entry.get().strip()
            if value:  # Only include non-empty fields
                columns.append(col)
                values.append(value)

        if not columns:
            tkmb.showerror("Error", "Please enter at least one field")
            return

        # Make API call
        try:
            with api_app.test_client() as client:
                response = client.post(
                    f"/tables/{table}",
                    json={"columns": columns, "rows": [values]}
                )
                result = response.get_json()

                if response.status_code == 200:
                    tkmb.showinfo("Success", result.get("message", "Data inserted successfully"))
                    # Clear input fields
                    for entry in input_fields.values():
                        entry.delete(0, 'end')
                else:
                    tkmb.showerror("Error", result.get("error", "Unknown error"))
        except Exception as e:
            tkmb.showerror("Error", f"Failed to insert data: {str(e)}")


def read_data(dashboard_window):
    '''
    Create a new window to read/view data from tables
    '''
    read_window = ctk.CTkToplevel(app)
    read_window.title("Read from Database")
    read_window.geometry("1200x800")
    # Center the window
    read_window.update_idletasks()
    screen_width = read_window.winfo_screenwidth()
    screen_height = read_window.winfo_screenheight()
    x = (screen_width - 1200) // 2
    y = (screen_height - 800) // 2
    read_window.geometry(f"1200x800+{x}+{y}")

    # Frames
    top_frame = ctk.CTkFrame(master=read_window)
    top_frame.pack(fill="x", pady=10, padx=10)
    middle_frame = ctk.CTkFrame(master=read_window)
    middle_frame.pack(fill="both", expand=True, pady=10, padx=10)
    bottom_frame = ctk.CTkFrame(master=read_window)
    bottom_frame.pack(fill="x", pady=10, padx=10)

    # Exit button
    exit_button = ctk.CTkButton(
        master=top_frame,
        text="← Back to Dashboard",
        command=lambda: [read_window.destroy(), dashboard_window.deiconify()],
        fg_color="gray",
        hover_color="darkgray"
    )
    exit_button.pack(side="left", padx=10, pady=10)

    # Dictionary of tables
    tables = {
        "department": ["department_id", "name", "description"],
        "district": ["district_id", "name", "description"],
        "topic": ["topic_id", "name", "description"],
        "gov_website": ["website_id", "name", "url", "department_id", "district_id", "topic_id"]
    }

    selected_table = ctk.StringVar(value="Select a table")

    table_label = ctk.CTkLabel(master=top_frame, text="Select Table:", font=("Arial", 14, "bold"))
    table_label.pack(side="left", padx=10)

    table_dropdown = ctk.CTkComboBox(
        master=top_frame,
        values=list(tables.keys()),
        variable=selected_table,
        width=300
    )
    table_dropdown.pack(side="left", pady=10)

    # Read button
    read_btn = ctk.CTkButton(
        master=top_frame,
        text="View Data",
        command=lambda: fetch_and_display_data(),
        fg_color="blue",
        hover_color="darkblue",
        width=120
    )
    read_btn.pack(side="left", padx=10)

    # Refresh button
    refresh_btn = ctk.CTkButton(
        master=top_frame,
        text="🔄 Refresh",
        command=lambda: fetch_and_display_data(),
        fg_color="green",
        hover_color="darkgreen",
        width=120
    )
    refresh_btn.pack(side="left", padx=5)

    def fetch_and_display_data():
        table = selected_table.get()
        if table == "Select a table":
            tkmb.showerror("Error", "Please select a table")
            return

        # Clear middle frame
        for widget in middle_frame.winfo_children():
            widget.destroy()

        try:
            with api_app.test_client() as client:
                response = client.get(f"/tables/{table}")
                result = response.get_json()

                if response.status_code == 200:
                    data = result.get("selected_tables", [])

                    # Create scrollable text box
                    text_box = ctk.CTkTextbox(master=middle_frame, width=800, height=500)
                    text_box.pack(pady=10, padx=10, fill="both", expand=True)

                    # Display column headers
                    columns = tables.get(table, [])
                    header = " | ".join([f"{col:20}" for col in columns])
                    text_box.insert("end", "=" * len(header) + "\n")
                    text_box.insert("end", header + "\n")
                    text_box.insert("end", "=" * len(header) + "\n\n")

                    # Display data
                    if data:
                        for row in data:
                            row_text = " | ".join([f"{str(val):20}" for val in row])
                            text_box.insert("end", row_text + "\n")

                        text_box.insert("end", f"\n{'-' * len(header)}\n")
                        text_box.insert("end", f"Total Rows: {len(data)}\n")
                    else:
                        text_box.insert("end", "\nNo data found in this table.\n")

                    text_box.configure(state="disabled")
                else:
                    tkmb.showerror("Error", result.get("error", "Failed to fetch data"))
        except Exception as e:
            tkmb.showerror("Error", f"Failed to read data: {str(e)}")


def update_data(dashboard_window):
    '''
    Create a new window to update data with WHERE and SET clauses
    '''
    update_window = ctk.CTkToplevel(app)
    update_window.title("Update Database")
    update_window.geometry("1200x800")
    # Center the window
    update_window.update_idletasks()
    screen_width = update_window.winfo_screenwidth()
    screen_height = update_window.winfo_screenheight()
    x = (screen_width - 1200) // 2
    y = (screen_height - 800) // 2
    update_window.geometry(f"1200x800+{x}+{y}")

    # Frames
    top_frame = ctk.CTkFrame(master=update_window)
    top_frame.pack(fill="x", pady=10, padx=10)
    middle_frame = ctk.CTkFrame(master=update_window)
    middle_frame.pack(fill="both", expand=True, pady=10, padx=10)
    bottom_frame = ctk.CTkFrame(master=update_window)
    bottom_frame.pack(fill="x", pady=10, padx=10)

    # Exit button
    exit_button = ctk.CTkButton(
        master=top_frame,
        text="← Back to Dashboard",
        command=lambda: [update_window.destroy(), dashboard_window.deiconify()],
        fg_color="gray",
        hover_color="darkgray"
    )
    exit_button.pack(side="left", padx=10, pady=10)

    # Dictionary of tables
    tables = {
        "department": ["department_id", "name", "description"],
        "district": ["district_id", "name", "description"],
        "topic": ["topic_id", "name", "description"],
        "gov_website": ["website_id", "name", "url", "department_id", "district_id", "topic_id"]
    }

    selected_table = ctk.StringVar(value="Select a table")

    table_label = ctk.CTkLabel(master=top_frame, text="Select Table:", font=("Arial", 14, "bold"))
    table_label.pack(side="left", padx=10)

    table_dropdown = ctk.CTkComboBox(
        master=top_frame,
        values=list(tables.keys()),
        variable=selected_table,
        width=300,
        command=lambda _=None: show_update_fields()
    )
    table_dropdown.pack(side="left", pady=10)

    where_fields = {}
    set_fields = {}

    def show_update_fields():
        # Clear previous widgets
        for widget in middle_frame.winfo_children():
            widget.destroy()
        for widget in bottom_frame.winfo_children():
            widget.destroy()

        table = selected_table.get()
        where_fields.clear()
        set_fields.clear()

        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(master=middle_frame, width=700, height=500)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # WHERE clause section
        where_label = ctk.CTkLabel(
            master=scroll_frame,
            text="WHERE Clause (Identify which row to update):",
            font=("Arial", 16, "bold"),
            text_color="orange"
        )
        where_label.pack(pady=10)

        where_instruction = ctk.CTkLabel(
            master=scroll_frame,
            text="Enter the column and value to identify the row (e.g., department_id = 1)",
            font=("Arial", 12)
        )
        where_instruction.pack(pady=5)

        # WHERE clause inputs
        for col in tables.get(table, []):
            where_frame = ctk.CTkFrame(master=scroll_frame)
            where_frame.pack(pady=3, padx=10, fill="x")

            label = ctk.CTkLabel(master=where_frame, text=f"{col}:", width=150, anchor="w")
            label.pack(side="left", padx=5)

            entry = ctk.CTkEntry(master=where_frame, width=400, placeholder_text=f"Value to match")
            entry.pack(side="left", padx=5)

            where_fields[col] = entry

        # Separator
        separator = ctk.CTkLabel(master=scroll_frame, text="─" * 80, font=("Arial", 14))
        separator.pack(pady=15)

        # SET clause section
        set_label = ctk.CTkLabel(
            master=scroll_frame,
            text="SET Clause (New values to update):",
            font=("Arial", 16, "bold"),
            text_color="green"
        )
        set_label.pack(pady=10)

        set_instruction = ctk.CTkLabel(
            master=scroll_frame,
            text="Enter the new values for columns you want to update",
            font=("Arial", 12)
        )
        set_instruction.pack(pady=5)

        # SET clause inputs
        for col in tables.get(table, []):
            set_frame = ctk.CTkFrame(master=scroll_frame)
            set_frame.pack(pady=3, padx=10, fill="x")

            label = ctk.CTkLabel(master=set_frame, text=f"{col}:", width=150, anchor="w")
            label.pack(side="left", padx=5)

            entry = ctk.CTkEntry(master=set_frame, width=400, placeholder_text=f"New value")
            entry.pack(side="left", padx=5)

            set_fields[col] = entry

        # Update button
        update_btn = ctk.CTkButton(
            master=bottom_frame,
            text="Update Data",
            command=submit_update,
            fg_color="orange",
            hover_color="darkorange"
        )
        update_btn.pack(pady=10)

    def submit_update():
        table = selected_table.get()
        if table == "Select a table":
            tkmb.showerror("Error", "Please select a table")
            return

        # Collect WHERE clause
        where_conditions = []
        for col, entry in where_fields.items():
            value = entry.get().strip()
            if value:
                where_conditions.append(f"{col} = '{value}'")

        if not where_conditions:
            tkmb.showerror("Error", "Please specify at least one WHERE condition")
            return

        # Collect SET clause
        set_values = []
        for col, entry in set_fields.items():
            value = entry.get().strip()
            if value:
                set_values.append(f"{col} = '{value}'")

        if not set_values:
            tkmb.showerror("Error", "Please specify at least one field to update")
            return

        # Build SQL query
        where_clause = " AND ".join(where_conditions)
        set_clause = ", ".join(set_values)
        sql_query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

        # Confirm with user
        confirm = tkmb.askyesno(
            "Confirm Update",
            f"This will execute:\n\n{sql_query}\n\nContinue?"
        )

        if confirm:
            try:
                db = database.init_db()
                cursor = db.cursor()
                cursor.execute(sql_query)
                db.commit()
                affected_rows = cursor.rowcount
                cursor.close()

                tkmb.showinfo("Success", f"{affected_rows} row(s) updated successfully")

                # Clear fields
                for entry in where_fields.values():
                    entry.delete(0, 'end')
                for entry in set_fields.values():
                    entry.delete(0, 'end')

            except Exception as e:
                tkmb.showerror("Error", f"Failed to update data: {str(e)}")


def delete_data(dashboard_window):
    '''
    Create a new window to delete data
    '''
    delete_window = ctk.CTkToplevel(app)
    delete_window.title("Delete from Database")
    delete_window.geometry("1200x800")
    # Center the window
    delete_window.update_idletasks()
    screen_width = delete_window.winfo_screenwidth()
    screen_height = delete_window.winfo_screenheight()
    x = (screen_width - 1200) // 2
    y = (screen_height - 800) // 2
    delete_window.geometry(f"1200x800+{x}+{y}")

    # Frames
    top_frame = ctk.CTkFrame(master=delete_window)
    top_frame.pack(fill="x", pady=10, padx=10)
    middle_frame = ctk.CTkFrame(master=delete_window)
    middle_frame.pack(fill="both", expand=True, pady=10, padx=10)
    bottom_frame = ctk.CTkFrame(master=delete_window)
    bottom_frame.pack(fill="x", pady=10, padx=10)

    # Exit button
    exit_button = ctk.CTkButton(
        master=top_frame,
        text="← Back to Dashboard",
        command=lambda: [delete_window.destroy(), dashboard_window.deiconify()],
        fg_color="gray",
        hover_color="darkgray"
    )
    exit_button.pack(side="left", padx=10, pady=10)

    # Dictionary of tables
    tables = {
        "department": ["department_id", "name", "description"],
        "district": ["district_id", "name", "description"],
        "topic": ["topic_id", "name", "description"],
        "gov_website": ["website_id", "name", "url", "department_id", "district_id", "topic_id"]
    }

    selected_table = ctk.StringVar(value="Select a table")

    table_label = ctk.CTkLabel(master=top_frame, text="Select Table:", font=("Arial", 14, "bold"))
    table_label.pack(side="left", padx=10)

    table_dropdown = ctk.CTkComboBox(
        master=top_frame,
        values=list(tables.keys()),
        variable=selected_table,
        width=300,
        command=lambda _=None: show_delete_fields()
    )
    table_dropdown.pack(side="left", pady=10)

    where_fields = {}

    def show_delete_fields():
        # Clear previous widgets
        for widget in middle_frame.winfo_children():
            widget.destroy()
        for widget in bottom_frame.winfo_children():
            widget.destroy()

        table = selected_table.get()
        where_fields.clear()

        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(master=middle_frame, width=600, height=400)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        title_label = ctk.CTkLabel(
            master=scroll_frame,
            text=f"Delete from {table}:",
            font=("Arial", 16, "bold"),
            text_color="red"
        )
        title_label.pack(pady=10)

        instruction = ctk.CTkLabel(
            master=scroll_frame,
            text="Enter conditions to identify rows to delete (WHERE clause):",
            font=("Arial", 12)
        )
        instruction.pack(pady=5)

        # Create WHERE condition inputs
        for col in tables.get(table, []):
            field_frame = ctk.CTkFrame(master=scroll_frame)
            field_frame.pack(pady=5, padx=10, fill="x")

            label = ctk.CTkLabel(master=field_frame, text=f"{col}:", width=150, anchor="w")
            label.pack(side="left", padx=5)

            entry = ctk.CTkEntry(master=field_frame, width=400, placeholder_text=f"Value to match")
            entry.pack(side="left", padx=5)

            where_fields[col] = entry

        # Delete button
        delete_btn = ctk.CTkButton(
            master=bottom_frame,
            text="Delete Data",
            command=submit_delete,
            fg_color="red",
            hover_color="darkred"
        )
        delete_btn.pack(pady=10)

    def submit_delete():
        table = selected_table.get()
        if table == "Select a table":
            tkmb.showerror("Error", "Please select a table")
            return

        # Collect WHERE clause
        where_conditions = []
        for col, entry in where_fields.items():
            value = entry.get().strip()
            if value:
                where_conditions.append(f"{col} = '{value}'")

        if not where_conditions:
            tkmb.showerror("Error", "Please specify at least one WHERE condition to delete safely")
            return

        # Build SQL query
        where_clause = " AND ".join(where_conditions)
        sql_query = f"DELETE FROM {table} WHERE {where_clause}"

        # Confirm with user
        confirm = tkmb.askyesno(
            "Confirm Delete",
            f"WARNING: This will permanently delete data!\n\nQuery:\n{sql_query}\n\nContinue?"
        )

        if confirm:
            try:
                db = database.init_db()
                cursor = db.cursor()
                cursor.execute(sql_query)
                db.commit()
                affected_rows = cursor.rowcount
                cursor.close()

                tkmb.showinfo("Success", f"{affected_rows} row(s) deleted successfully")

                # Clear fields
                for entry in where_fields.values():
                    entry.delete(0, 'end')

            except Exception as e:
                tkmb.showerror("Error", f"Failed to delete data: {str(e)}")


def generate_reports(dashboard_window):
    '''
    Create a new window to generate reports
    '''
    report_window = ctk.CTkToplevel(app)
    report_window.title("Generate Reports")
    report_window.geometry("1200x800")
    # Center the window
    report_window.update_idletasks()
    screen_width = report_window.winfo_screenwidth()
    screen_height = report_window.winfo_screenheight()
    x = (screen_width - 1200) // 2
    y = (screen_height - 800) // 2
    report_window.geometry(f"1200x800+{x}+{y}")

    # Frames
    top_frame = ctk.CTkFrame(master=report_window)
    top_frame.pack(fill="x", pady=10, padx=10)
    middle_frame = ctk.CTkFrame(master=report_window)
    middle_frame.pack(fill="both", expand=True, pady=10, padx=10)
    bottom_frame = ctk.CTkFrame(master=report_window)
    bottom_frame.pack(fill="x", pady=10, padx=10)

    # Exit button
    exit_button = ctk.CTkButton(
        master=top_frame,
        text="← Back to Dashboard",
        command=lambda: [report_window.destroy(), dashboard_window.deiconify()],
        fg_color="gray",
        hover_color="darkgray"
    )
    exit_button.pack(side="left", padx=10, pady=10)

    label = ctk.CTkLabel(
        master=middle_frame,
        text="Report Generation Feature - Coming Soon!",
        font=("Arial", 20, "bold")
    )
    label.pack(expand=True)


def list_websites(dashboard_window):
    '''
    Create a new window to list all government websites
    '''
    website_window = ctk.CTkToplevel(app)
    website_window.title("List Websites")
    website_window.geometry("1200x800")
    # Center the window
    website_window.update_idletasks()
    screen_width = website_window.winfo_screenwidth()
    screen_height = website_window.winfo_screenheight()
    x = (screen_width - 1200) // 2
    y = (screen_height - 800) // 2
    website_window.geometry(f"1200x800+{x}+{y}")

    # Frames
    top_frame = ctk.CTkFrame(master=website_window)
    top_frame.pack(fill="x", pady=10, padx=10)
    middle_frame = ctk.CTkFrame(master=website_window)
    middle_frame.pack(fill="both", expand=True, pady=10, padx=10)

    # Exit button
    exit_button = ctk.CTkButton(
        master=top_frame,
        text="← Back to Dashboard",
        command=lambda: [website_window.destroy(), dashboard_window.deiconify()],
        fg_color="gray",
        hover_color="darkgray"
    )
    exit_button.pack(side="left", padx=10, pady=10)

    # Fetch and display websites
    try:
        with api_app.test_client() as client:
            response = client.get("/websites")
            result = response.get_json()

            if response.status_code == 200:
                urls = result.get("urls", [])

                text_box = ctk.CTkTextbox(master=middle_frame, width=800, height=500)
                text_box.pack(pady=10, padx=10, fill="both", expand=True)

                text_box.insert("end", "Government Websites:\n")
                text_box.insert("end", "=" * 80 + "\n\n")

                if urls:
                    for i, url in enumerate(urls, 1):
                        text_box.insert("end", f"{i}. {url}\n")
                else:
                    text_box.insert("end", "No websites found.\n")

                text_box.configure(state="disabled")
            else:
                tkmb.showerror("Error", result.get("error", "Failed to fetch websites"))
    except Exception as e:
        tkmb.showerror("Error", f"Failed to list websites: {str(e)}")


# WIDGETS
# Login Window
heading_label = ctk.CTkLabel(app, text="Welcome to the Government Website Database")
heading_label.pack(pady=20)
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)
login_label = ctk.CTkLabel(master=frame, text='MASU - Modern Authentication System UI')
login_label.pack(pady=12, padx=10)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
user_entry.pack(pady=12, padx=10)
user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
user_pass.pack(pady=12, padx=10)

login_button = ctk.CTkButton(master=frame, text='Login', command=login)
login_button.pack(pady=12, padx=10)

# Menu Bar
option_menu = Menu(app)
app.config(menu=option_menu)

file_menu = Menu(option_menu, tearoff=0)

file_menu.add_command(label="Exit", command=app.destroy)
file_menu.add_separator()
option_menu.add_cascade(label="File", menu=file_menu)

# main event loop, must be at EOF
app.mainloop()