import sqlite3

class Account():
    def __init__(self, root, gui_instance, db_instance):
        self.root = root
        self.gui = gui_instance
        self.db = db_instance

    # Define the method to handle the login logic
    def perform_login(self, username, password):

        #username = self.gui.username_entry.get() # Retrieve the username from the username entry widget
        #password = self.gui.pw_entry.get() # Retrieve the password from the password entry widget

        # Attempt to authenticate the user with the provided username and password
        # authenticate_user returns a tuple containing profile data and an error message (if any)
        profile_data, error_message = self.db.authenticate_user(username, password)

        self.username = username # Set the username attribute of the class to the entered username
        self.profile_id = username  

        # If profile data is received, the login is successful
        if profile_data:
            print("Login successful!")
            # Reiterate setting the username attribute for clarity or potential previous misuse
            self.username = username
            # Offer the user options for next steps
            self.gui.menu_page()
        # If no profile data is found for the user, inform them and direct to add a new website
        elif error_message == "No profile data found for the user.":
            print("No profile data found for the user.")
            self.gui.add_website_page()
        # If login failed due to other errors, inform the user and display the error message
        else:
            print("Login failed. Please try again.")
            print("Error:", error_message)
            # Show the error message using a custom method
            self.gui.show_message("error", error_message)

    # Define the method to handle the signup process
    def perform_signup(self, username, pw, cpw): 
        # Retrieve the username entered by the user
        new_username = username
        # Retrieve the password entered by the user
        new_password = pw
        # Retrieve the confirmation password entered by the user
        confirm_password = cpw
        
        self.username = new_username
        
        # The user must put a username and password
        if new_username == '' or new_password == '':
            self.gui.show_message("error", "You must have a username and password")
            return

        # Check if the entered password and confirmation password match
        if new_password != confirm_password:
            # If they don't match, print an error message
            self.gui.show_message("error", "The passwords entered do not match. Please try again")
            return

        # Attempt to create a new user with the provided credentials
        try:
            # This function attempts to insert a new user record into the database
            # It will raise an sqlite3.IntegrityError if the username already exists
            self.db.insert_new_user(new_username, new_password)
            self.gui.show_message("success", "New user has been created") # If the insertion is successful, display a success message
            print("User signed up successfully!")
            
            self.gui.show_menu() #Opens the main menu page
        # Handle the case where the username already exists in the database
        except sqlite3.IntegrityError:
            # Display an error message prompting the user to choose a different username
            self.gui.show_message("error", "Username already exists. Please choose a different username.")
