from tkinter import messagebox
import sqlite3
from DB import authenticate_user, insert_new_user

def login_page(root, username_entry, pw_entry):
    def perform_login():
        # Authenticate the user
        username = username_entry.get()
        password = pw_entry.get()
        profile_data, error_message = authenticate_user(username, password)

        if profile_data:
            messagebox.showinfo("Success", "Login successful!")
            # You can navigate to another page or display a message
        else:
            messagebox.showerror("Error", "Login failed. Please try again.")

    login_btn = CTkButton(root, text="Log In", command=perform_login)
    login_btn.pack()

def signup_page(root, username_entry, pw_entry, confirm_pw_entry):
    def perform_signup():
        new_username = username_entry.get()
        new_password = pw_entry.get()
        confirm_password = confirm_pw_entry.get()

        # Check if passwords match
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords don't match!")
            return
        
        try:
            # Insert the new user into the database
            insert_new_user(new_username, new_password)
            messagebox.showinfo("Success", "User signed up successfully!")
        except sqlite3.IntegrityError:
            # Username already exists, show error message
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")

    signup_btn = CTkButton(root, text="Sign Up", command=perform_signup)
    signup_btn.pack()

def clear_widgets(root):
    # Destroy all widgets in the root window
    for widget in root.winfo_children():
        widget.destroy()
