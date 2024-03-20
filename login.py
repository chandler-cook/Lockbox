from ui import *


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
