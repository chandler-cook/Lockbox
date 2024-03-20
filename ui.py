from tkinter import *
from tkinter import messagebox
from customtkinter import *
import customtkinter
from DB import *


class LockboxApp:
    def __init__(self, root):
        self.root = root
        self.username = None  # Initialize username
        self.profile_id = None
        self.startup_page()

    # Define the startup page setup method
    def startup_page(self):
        # Clear any existing widgets from the interface to start fresh
        self.clear_widgets()

        # Create a label widget for the application title "Lockbox"
        lockbox_label = CTkLabel(self.root, text="Lockbox", font=('Arial', 30))
        # Add the lockbox_label to the application window using pack geometry manager, which organizes widgets in a block
        lockbox_label.pack()

        # Create a descriptive label widget below the application title
        desc_label = CTkLabel(self.root, text="a password manager", font=('Arial', 15))
        # Add the desc_label to the application window below the title label
        desc_label.pack()

        # Create a button widget for logging in
        # The command parameter is set to self.login_page, which means
        # clicking this button will execute the login_page method, navigating to the login interface
        login_btn = CTkButton(self.root, text="Log In", command=self.login_page)
        # Add the login button to the application window, below the description label
        login_btn.pack()

        # Create a button widget for signing up
        # Clicking this button executes the signup_page method, leading to the sign-up interface
        signup_btn = CTkButton(self.root, text="Sign Up", command=self.signup_page)
        # Add the signup button to the application window, below the login button
        signup_btn.pack()

    # Define the method for displaying the login page
    def login_page(self):
        # Clear any existing widgets to prepare for displaying the login interface
        self.clear_widgets()

        # Create a label widget for the login page title "Log In"
        login_label = CTkLabel(self.root, text="Log In")
        # Add the login_label to the application window using pack geometry manager
        login_label.pack()

        # This uses a custom entry class CTkEntry and displays "Username" as placeholder text
        self.username_entry = CTkEntry(self.root, placeholder_text="Username")
        # Add the username entry field to the application window
        self.username_entry.pack()

        # Create an entry widget for the password input
        # It also uses CTkEntry but hides the entered text with asterisks (*) for privacy
        self.pw_entry = CTkEntry(self.root, placeholder_text="Password", show='*')
        # Add the password entry field to the application window
        self.pw_entry.pack()

        # Create a button for submitting the login information
        # This button is labeled "Log In" and is linked to the self.perform_login method
        # which attempts to authenticate the user with the entered credentials
        login_btn = CTkButton(self.root, text="Log In", command=self.perform_login)
        # Add the login button to the application window
        login_btn.pack()

        # Create a back button for returning to the startup page
        # linked to the self.startup_page method by the ←
        # allowing the user to go back to the initial screen of the application
        back_button = CTkButton(self.root, text="←", command=self.startup_page)
        # Add the back button to the application window
        back_button.pack()

    # Define the method to handle the login logic
    def perform_login(self):
        # Retrieve the username from the username entry widget
        username = self.username_entry.get()
        # Retrieve the password from the password entry widget
        password = self.pw_entry.get()

        # Attempt to authenticate the user with the provided username and password
        # `authenticate_user` returns a tuple containing profile data and an error message (if any)
        profile_data, error_message = authenticate_user(username, password)

        # Set the username attribute of the class to the entered username
        self.username = username
        self.profile_id = username  

        # If profile data is received, the login is successful
        if profile_data:
            print("Login successful!")
            # Reiterate setting the username attribute for clarity or potential previous misuse
            self.username = username
            # Offer the user options for next steps
            self.show_menu()
            # print("Would you like to:")
            # print("1. View existing websites")
            # print("2. Add a new website")
            
            # Get the user's choice through input
            #choice = input("Enter your choice (1 or 2): ")
            # If choice is 1, call the method to view existing websites
            # if choice == "1":
            #     self.view_websites_page()
            # If choice is 2, call the method to add a new website
            # elif choice == "2":
            #     self.add_website_page()
            # Handle invalid choices by informing the user
            # else:
            #     print("Invalid choice. Please enter 1 or 2.")
        # If no profile data is found for the user, inform them and direct to add a new website
        elif error_message == "No profile data found for the user.":
            print("No profile data found for the user.")
            self.add_website_page()
        # If login failed due to other errors, inform the user and display the error message
        else:
            print("Login failed. Please try again.")
            print("Error:", error_message)
            # Show the error message using a custom method
            self.show_message("error", error_message)

    # Define the method to display the sign-up page
    def signup_page(self):
        # First, clear any existing widgets from the display
        # This ensures that the sign-up page starts with a clean slate
        self.clear_widgets()

        # Create and display a label indicating this page is for user sign-up
        signup_label = CTkLabel(self.root, text="Sign Up")
        signup_label.pack()

        # Set up an entry widget for the user to input a username
        # Placeholder text "Username" is displayed when the entry is empty
        self.username_entry = CTkEntry(self.root, placeholder_text="Username")
        self.username_entry.pack()

        # Set up a password entry widget
        # The entered text is obscured (shown as '*') for privacy
        self.pw_entry = CTkEntry(self.root, placeholder_text="Password", show='*')
        self.pw_entry.pack()

        # Set up another password entry widget for password confirmation
        # This also obscures entered text and serves to verify the user typed their password correctly
        self.confirm_pw_entry = CTkEntry(self.root, placeholder_text="Confirm Password", show='*')
        self.confirm_pw_entry.pack()

        # Create a sign-up button that, when clicked, calls the perform_signup method
        # This method is presumably responsible for processing the sign-up information
        signup_btn = CTkButton(self.root, text="Sign Up", command=self.perform_signup)
        signup_btn.pack()

        # Create a back button allowing users to return to the previous page (likely the startup page)
        # This is helpful in case the user decides not to sign up or wants to return to the login page
        back_button = CTkButton(self.root, text="←", command=self.startup_page)
        back_button.pack()

    # Define the method to handle the signup process
    def perform_signup(self):
        # Retrieve the username entered by the user
        new_username = self.username_entry.get()
        # Retrieve the password entered by the user
        new_password = self.pw_entry.get()
        # Retrieve the confirmation password entered by the user
        confirm_password = self.confirm_pw_entry.get()

        # The user must put a username and password
        if new_username == '' or new_password == '':
            self.show_message("error", "You must have a username and password")
            return

        # Check if the entered password and confirmation password match
        if new_password != confirm_password:
            # If they don't match, print an error message
            self.show_message("error", "The passwords entered do not match. Please try again")
            return

        # Attempt to create a new user with the provided credentials
        try:
            # This function attempts to insert a new user record into the database
            # It will raise an sqlite3.IntegrityError if the username already exists
            insert_new_user(new_username, new_password)
            # If the insertion is successful, display a success message
            self.show_message("success", "New user has been created")
            print("User signed up successfully!")
            #Opens the main menu page
            self.show_menu()
        # Handle the case where the username already exists in the database
        except sqlite3.IntegrityError:
            # Display an error message prompting the user to choose a different username
            self.show_message("error", "Username already exists. Please choose a different username.")

    # Define the method to display the main menu options to the user
    def show_menu(self):
        # Clear any existing widgets to prepare for displaying new options
        self.clear_widgets()

        # Check if there's website data associated with the user's profile
        if not self.check_website_data():
            # If no website data is found, provide an option to add a new website
            # This creates a button labeled "Add New Website"
            # Clicking this button will invoke the add_website_page method, leading the user to a page
            # where they can enter details for a new website
            add_website_btn = CTkButton(self.root, text="Add New Website", command=self.add_website_page)
            # Display the button using pack geometry manager, which adds it to the application window
            add_website_btn.pack()

        # Regardless of whether website data exists, provide an option to view websites
        # This creates a button labeled "View Websites"
        # Clicking this button will invoke the view_websites_page method, allowing the user to see a list
        # of websites associated with their account
        view_websites_btn = CTkButton(self.root, text="View Websites", command=self.view_websites_page)
        # Display this button as well, so the user can choose to view existing website data
        view_websites_btn.pack()

    # Define a method to display the page for adding new website information
    def add_website_page(self):
        # Clear any previously displayed widgets to prepare for new content
        self.clear_widgets()

        # Create and display a label to indicate this page is for adding new website details
        website_label = CTkLabel(self.root, text="Add New Website")
        website_label.pack()

        # Set up an entry widget for the user to input the name of the website
        self.website_name_entry = CTkEntry(self.root, placeholder_text="Website Name")
        self.website_name_entry.pack()

        # Set up an entry widget for the user to input their username for the website
        self.website_username_entry = CTkEntry(self.root, placeholder_text="Username")
        self.website_username_entry.pack()

        # Set up an entry widget for the user to input their password for the website
        # Entered text is obscured (shown as '*') for privacy
        self.website_pw_entry = CTkEntry(self.root, placeholder_text="Password", show='*')
        self.website_pw_entry.pack()

        # Create a button labeled "Save" that, when clicked, calls the save_website_details method
        # This method is presumably responsible for processing and storing the entered website information
        save_btn = CTkButton(self.root, text="Save", command=self.save_website_details)
        save_btn.pack()

        # Create a back button that allows users to return to the main menu
        # This provides a convenient way to navigate away from the add website page without saving
        back_button = CTkButton(self.root, text="←", command=self.show_menu)
        back_button.pack()

    # Define the method to save new website details entered by the user
    def save_website_details(self):
        # Retrieve the entered website name from the website name entry widget
        website_name = self.website_name_entry.get()
        # Retrieve the entered username for the website from the username entry widget
        website_username = self.website_username_entry.get()
        # Retrieve the entered password for the website from the password entry widget
        website_password = self.website_pw_entry.get()

        # Retrieve the current user's username from the stored attribute to associate with the website details
        username = self.username

        # Call the method to get the account ID for the current user based on their username
        # This is necessary to relate the website details with the specific user account in the database
        account_id = self.get_user_account_id(username)

        # Attempt to insert the new website details into the database
        try:
            # This method attempts to insert a new row into the database table for websites
            # It includes the current username, website name, website username, and password as parameters
            self.insert_new_website(self.username, website_name, website_username, website_password)
            # If the insert is successful, print a confirmation message
            print("Website details saved successfully!")
        # Handle any exceptions that occur during the database insert operation
        except Exception as e:
            # If an exception occurs, show an error message with the exception details
            self.show_message("error", "Failed to save website details. Error: " + str(e))

    # Define the method to display the webpage credentials associated with the user
    def view_websites_page(self):
        # Clear the current GUI widgets to prepare for new content
        self.clear_widgets()

        # Establish a connection to the SQLite database named 'lockbox.db'
        con = sqlite3.connect("lockbox.db")
        # Create a cursor object to execute SQL queries
        cur = con.cursor()

        # Execute a SQL query to select website name, username, and password
        # for all entries associated with the current user's lockbox account
        cur.execute("SELECT website_name, website_username, website_password FROM websites WHERE lockbox_account_id = (SELECT id FROM lockbox_accounts WHERE username = ?)", (self.username,))
        # Fetch all rows of the query result, storing them in `self.website_data`
        self.website_data = cur.fetchall()

        # Close the database connection to free resources
        con.close()

        # Check if any website data was found for the user
        if self.website_data:
            # If data is found, display a label indicating the following content will be the user's websites
            website_label = CTkLabel(self.root, text="Your Websites:")
            website_label.pack()

            # Loop through each website data entry
            for website in self.website_data:
                # Unpack the website information
                website_name, website_username, website_password = website
                # Format the website information into a string
                website_info = f"Website: {website_name}, Username: {website_username}, Password: {website_password}"
                # Display the website information as a label in the GUI
                website_info_label = CTkLabel(self.root, text=website_info)
                website_info_label.pack()
        else:
            # If no website data was found for the user, display a message indicating so
            no_website_label = CTkLabel(self.root, text="No websites found.")
            no_website_label.pack()

        # Add a back button to the GUI that, when clicked, will call the `show_menu` method
        # to return the user to the main menu
        back_button = CTkButton(self.root, text="← Back to Menu", command=self.show_menu)
        back_button.pack()

    # Define a method to check if website data exists for the user's account
    def check_website_data(self):
        # Establish a connection to the SQLite database named 'lockbox.db'
        con = sqlite3.connect("lockbox.db")
        # Create a cursor object to execute SQL commands
        cur = con.cursor()

        # Execute a SQL query to select all entries from the 'websites' table
        # where the 'lockbox_account_id' matches the user's profile ID
        cur.execute("SELECT * FROM websites WHERE lockbox_account_id = ?", (self.profile_id,))
        # Fetch all rows of the query result
        website_data = cur.fetchall()

        # Close the database connection to free resources
        con.close()

        # Convert the website_data to a boolean and return it
        # This will be True if website_data contains any entries, False otherwise
        return bool(website_data)

    # Define a method to display an error message in a graphical message box
    def show_message(self, message_type, message):
        # Call the messagebox's show<message type> function to display a dialog box
        # The first parameter is the title of the message box
        # The `message` parameter contains the message text to be displayed
        if message_type == "error" or "Error":
            messagebox.showerror("Error", message)
        elif message_type == "success" or "Success":
            messagebox.showinfo("Success", message)

    # Define a method to remove all child widgets from the root widget
    def clear_widgets(self):
        # Loop through each widget that is a child of the root widget
        for widget in self.root.winfo_children():
            # Destroy the widget, effectively removing it from the GUI
            widget.destroy()

    # Define a method to fetch the account ID for a given username from the database
    def get_user_account_id(self, username):
        try:
            # Establish a connection to the SQLite database named 'lockbox.db'
            con = sqlite3.connect("lockbox.db")
            # Create a cursor object to execute SQL commands
            cur = con.cursor()

            # Execute a SQL query to select the ID from the 'lockbox_accounts' table
            # where the 'username' column matches the provided username
            cur.execute("SELECT id FROM lockbox_accounts WHERE username = ?", (username,))
            # Fetch the first row of the results
            result = cur.fetchone()

            # Check if a result was found
            if result:
                return result[0]  # Return the account ID (first column of the row) if found
            else:
                return None  # Return None if there was no match for the username
        except sqlite3.Error as e:
            # Catch and print any SQLite error encountered during the operation
            print("Error while retrieving user account ID:", e)
            return None  # Return None in case of error
        finally:
            # Ensure that the database connection is closed to free resources
            if con:
                con.close()

    # Define a method to insert new website credentials into the database for a given user
    def insert_new_website(self, username, website_name, website_username, website_password):
        # Establish a connection to the SQLite database named 'lockbox.db'
        con = sqlite3.connect("lockbox.db")
        # Create a cursor object to execute SQL commands
        cur = con.cursor()

        # Execute a SQL query to select the ID of the user ('lockbox_account_id') from the 'lockbox_accounts' table
        # based on the provided username
        cur.execute("SELECT id FROM lockbox_accounts WHERE username=?", (username,))
        # Fetch the first row of the result set (if any)
        account_id = cur.fetchone()

        # If no account ID was found for the given username, print an error message, close the database connection,
        # and return False to indicate failure
        if account_id is None:
            print(f"No account found for username: {username}")
            con.close()
            return False

        # If the account ID is found, proceed to insert the new website information into the 'websites' table
        # The insertion includes the account ID, website name, website username, and password
        cur.execute("""
            INSERT INTO websites (lockbox_account_id, website_name, website_username, website_password)
            VALUES (?, ?, ?, ?)
        """, (account_id[0], website_name, website_username, website_password))
        # Commit the transaction to save changes to the database
        con.commit()
        # Close the database connection to free resources
        con.close()
        # Return True to indicate success
        return True


# Create and run the application
root = CTk()
root.geometry("500x300")
root.title("Lockbox")

# Sets default appearance and theme of window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Creating an instance of the LockboxApp class, passing the root window as a parameter.
# This step initializes the application with the root window as its main interface.
app = LockboxApp(root)

root.mainloop()
