import sqlite3
import string
import secrets
import pyperclip
import random
import bcrypt

class Account():
    def __init__(self, root, gui_instance, db_instance):
        self.root = root
        self.gui = gui_instance
        self.db = db_instance

    # Define the method to handle the login logic
    def perform_login(self, username, password):

        un = username # Retrieve the username from sent parameters
        pw = password # Retrieve the password from sent parameters

        # Attempt to authenticate the user with the provided username and password
        # authenticate_user returns a tuple containing profile data and an error message (if any)
        profile_data, error_message = self.db.authenticate_user(un, pw) 

        # If profile data is received, the login is successful
        if profile_data:
            
            print("Login successful!")
            # Offer the user options for next steps
            self.gui.menu_page(un)
        # If no profile data is found for the user, inform them and direct to add a new website
        elif error_message == "No profile data found for the user.":
            print("No profile data found for the user.")
            self.gui.add_website_page(un)
        # If login failed due to other errors, inform the user and display the error message
        else:
            print("Login failed. Please try again.")
            print("Error:", error_message)
            # Show the error message using a custom method
            self.gui.show_message("error", error_message)

    # Define the method to handle the signup process
    def perform_signup(self, username, password, confirm_password): 
        # Retrieve the username entered by the user
        un = username
        # Retrieve the password entered by the user
        pw = password
        # Retrieve the confirmation password entered by the user
        cpw = confirm_password
        
        # The user must put a username and password
        if un == '' or pw == '':
            self.gui.show_message("error", "You must have a username and password")
            return

        # Check if the entered password and confirmation password match
        if pw != cpw:
            # If they don't match, print an error message
            self.gui.show_message("error", "The passwords entered do not match. Please try again")
            return
        
        # Check if the username already exists
        if self.db.check_user(un):
            # If the username already exists, display an error message
            self.gui.show_message("error", "Username already exists. Please choose a different username.")
            return

        # Attempt to create a new user with the provided credentials
        try:
            # This function attempts to insert a new user record into the database
            # It will raise an sqlite3.IntegrityError if the username already exists
            self.db.insert_user(un, pw)
            self.gui.show_message("success", "New user has been created") # If the insertion is successful, display a success message
            print("User signed up successfully!")
            self.gui.login_page() #Opens the main menu page
        # Handle the case where the username already exists in the database
        except Exception as e:
            # Handle any other exceptions that might occur during the signup process
            self.gui.show_message("error", f"Failed to sign up. Error: {str(e)}")

    # Method for generating a password based on the parameters set by the user
    def generate_pass(self, username, length, upper, lower, digit, special):
        
        un = username
        
        pass_len = int(length.get()) # Password length variable
        
        # Variables holding value of checked boxes (1 = checked, 0 = unchecked)
        upperVar = upper.get()
        lowerVar = lower.get()
        digitVar = digit.get()
        specialVar = special.get()
        
        #Initialize character bank and blank new password list for generation
        char_bank = ''
        new_pass = []

        if (upperVar+lowerVar+digitVar+specialVar) == 0:
            self.gui.show_message('error', 'You must select at least one password option to generate a new password.\nPlease try again.')
            self.gui.generate_pass_page(un)
            return
        
        # IF structure for determining what characters to include in the character bank the generator will chose from
        # Also ensures there is at least one instance of each user specified character
        if upperVar == 1:
            # If "Inlcude Uppercase letter" box is checked, include all uppercase letters in the character bank,
            # and add one uppercase letter to the new password, same for rest
            char_bank = string.ascii_uppercase
            new_pass.append(secrets.choice(string.ascii_uppercase))
        if lowerVar == 1:
            char_bank += string.ascii_lowercase
            new_pass.append(secrets.choice(string.ascii_lowercase))
        if digitVar == 1:
            char_bank += string.digits
            new_pass.append(secrets.choice(string.digits))
        if specialVar == 1:
            char_bank += string.punctuation
            new_pass.append(secrets.choice(string.punctuation))
        # Fill the rest of the password with random characters from the combined character bank
        while len(new_pass) < pass_len:    
            new_pass.append(secrets.choice(char_bank))
        # Shuffle the password to mix the initial characters
        random.shuffle(new_pass)
        # Convert the list of characters back into a string
        new_pass = ''.join(new_pass)    
        
        pyperclip.copy(new_pass) # Copies the Generated password to user's clipboard
        
        # Success Message
        self.gui.show_message("success", f"Your generated password is: {new_pass}\nYour password has been automaticaly copied to the clipboard." )
        
        # Go back to main menu after exiting success message
        self.gui.menu_page(un)

    def hash_pass(self, password):
        
        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        return hashed_password