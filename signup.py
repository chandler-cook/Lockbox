from ui import *

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
        
        self.username = new_username
        

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
