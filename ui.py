# modules
from tkinter import *
from tkinter import messagebox
from customtkinter import *
from DB import *

# Defining the LockboxApp class
class LockboxApp:
    
# Beginning of logic
    def __init__(self, root):
        # Initialize the LockboxApp with the root window
        self.root = root
        # Start with the startup page
        self.startup_page()
        
# First GUI page shown to chose login or create new user
    def startup_page(self):
        # Clear existing widgets from the root window
        self.clear_widgets()

        # Create labels and buttons for the startup page
        lockbox_label = CTkLabel(self.root, text="Lockbox", font=('Arial', 30))
        lockbox_label.pack()

        desc_label = CTkLabel(self.root, text="a password manager", font=('Arial', 15))
        desc_label.pack()

        login_btn = CTkButton(self.root, text="Log In", command=self.login_page)
        login_btn.pack()

        signup_btn = CTkButton(self.root, text="Sign Up", command=self.signup_page)
        signup_btn.pack()

# GUI login page function
    def login_page(self):
        # Clear existing widgets from the root window
        self.clear_widgets()

        # Create labels, entry fields, and buttons for the login page
        login_label = CTkLabel(self.root, text="Log In")
        login_label.pack()

        self.username_entry = CTkEntry(self.root, placeholder_text="Username")
        self.username_entry.pack()

        self.pw_entry = CTkEntry(self.root, placeholder_text="Password", show='*')
        self.pw_entry.pack()

        login_btn = CTkButton(self.root, text="Log In", command=self.perform_login)
        login_btn.pack()

        back_button = CTkButton(self.root, text="←", command=self.startup_page)
        back_button.pack()


# Function to implement the actual login logic
    def perform_login(self):
        username = self.username_entry.get()
        password = self.pw_entry.get()

        profile_data, error_message = authenticate_user(username, password)

        if profile_data:
            print("Login successful!")
            self.website_details_page()  # Navigate to the website details page
        else:
            print("Login failed. Please try again.")
            if error_message == "No profile data found for the user.":
                print("No profile data found. Redirecting to website details page.")
                self.website_details_page()  # Call website details page directly
            else:
                self.show_error_message(error_message)

    
    def website_details_page(self):
        self.clear_widgets()

        website_label = CTkLabel(self.root, text="Website Name")
        website_label.pack()

        self.website_entry = CTkEntry(self.root, placeholder_text="Enter website name")
        self.website_entry.pack()

        username_label = CTkLabel(self.root, text="Username")
        username_label.pack()

        self.username_entry = CTkEntry(self.root, placeholder_text="Enter username")
        self.username_entry.pack()

        pw_label = CTkLabel(self.root, text="Password")
        pw_label.pack()

        self.pw_entry = CTkEntry(self.root, placeholder_text="Enter password", show='*')
        self.pw_entry.pack()

        save_btn = CTkButton(self.root, text="Save", command=self.save_website_details)
        save_btn.pack()

        back_button = CTkButton(self.root, text="←", command=self.startup_page)
        back_button.pack()

    def save_website_details(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.pw_entry.get()

        # Check if the user already has a profile
        existing_profile_data, _ = authenticate_user(username, "")  # Empty password to check only username existence

        if existing_profile_data:
            # User has an existing profile, insert website details into the existing profile
            insert_new_profile(username, website, username, password)
            print("Website details saved successfully!")
        else:
            # User does not have an existing profile, create a new profile and insert website details
            try:
                insert_new_user(username, "")  # Empty password to create a new profile
                insert_new_profile(username, website, username, password)
                print("New profile and website details saved successfully!")
            except sqlite3.IntegrityError:
                self.show_error_message("Failed to create a new profile.")

     
# Function to present error message in GUI       
    def show_error_message(self, message):  # Define show_error_message within the class
        # Show error message using tkinter messagebox
        messagebox.showerror("Error", message)


# Function to show sign up page
    def signup_page(self):
        # Clear existing widgets from the root window
        self.clear_widgets()

        # Create labels, entry fields, and buttons for the signup page
        signup_label = CTkLabel(self.root, text="Sign Up")
        signup_label.pack()

        self.username_entry = CTkEntry(self.root, placeholder_text="Username")
        self.username_entry.pack()

        self.pw_entry = CTkEntry(self.root, placeholder_text="Password", show='*')
        self.pw_entry.pack()

        self.confirm_pw_entry = CTkEntry(self.root, placeholder_text="Confirm Password", show='*')
        self.confirm_pw_entry.pack()

        signup_btn = CTkButton(self.root, text="Sign Up", command=self.perform_signup)
        signup_btn.pack()

        back_button = CTkButton(self.root, text="←", command=self.startup_page)
        back_button.pack()



# Function to signup a new account
    def perform_signup(self):
        # Get new username, password, and confirm password
        new_username = self.username_entry.get()
        new_password = self.pw_entry.get()
        confirm_password = self.confirm_pw_entry.get()

        # Check if passwords match
        if new_password != confirm_password:
            print("Passwords don't match!")
            return

        try:
            # Insert new user into the database using DB module
            insert_new_user(new_username, new_password)
            print("User signed up successfully!")
        except sqlite3.IntegrityError:
            # Show error message if username already exists
            self.show_error_message("Username already exists. Please choose a different username.")



# Clear all existing widgets from the root window 
    # Retrieve a list of all child widgets of the root window
    # using the winfo_children() method, which returns a list of
    # all the children of a widget
    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy() # Destroy each widget in the list


# Create the root window
root = CTk()
root.geometry("500x300")
root.title("Lockbox")

# Initialize the LockboxApp with the root window
app = LockboxApp(root)

# Start the tkinter event loop
root.mainloop()
