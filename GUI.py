from ui import *
from signup import *
from login import *

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
