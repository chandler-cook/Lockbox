from customtkinter import *
from tkinter import messagebox
import sqlite3


class GUI():
    def __init__(self, root, account_instance, db_instance):
        self.root = root
        self.account = account_instance
        self.db = db_instance
        self.curr_page = None
        self.startup_page()
        self.root.bind("<Return>", self.on_enter_press) # Binds the action of pressing enter/return key to calling the on_enter_press method to be used by the window
        #=========================================================================================================================
        # **NOTE**: There is an error in the terminal anytime the user presses the 
        # enter/return key outside of the the login/signup page. This was happening before I implemented
        # the enter key functionality. Not sure if there is a way to remove this, but press the enter key
        # in any page besides the login/signup page, and you will see error in terminal.
        # This doesn't hinder user experience, simply an annoying message in the terminal, is it possible to get rid of tho?

    # Define a method to remove all child widgets from the root widget
    def clear_widgets(self):
        # Loop through each widget that is a child of the root widget
        for widget in self.root.winfo_children():
            # Destroy the widget, effectively removing it from the GUI
            widget.destroy()

    # Define a method to display an error message in a graphical message box
    def show_message(self, message_type, message):
        # Call the messagebox's show<message type> function to display a dialog box
        # The first parameter is the title of the message box
        # The `message` parameter contains the message text to be displayed
        if message_type == "error" or message_type == "Error":
            messagebox.showerror("Error", message)
        elif message_type == "success" or  message_type == "Success":
            messagebox.showinfo("Success", message)

    # Defines a method to specify any button they wish to be made pressable by the enter key
    def on_enter_press(self, event):
        # If the user is on a certain page, defined by a page identifier, then invoke a specified button
        if self.curr_page == 'login':
            self.login_btn.invoke()
        elif self.curr_page == 'signup':
            self.signup_btn.invoke()
        elif self.curr_page == 'addwebsite':
            self.save_btn.invoke()
        elif self.curr_page == 'genpass':
            self.generate_pass_btn.invoke()
        elif self.curr_page == "menu":
            pass
        # To add more enter key functionality for buttons, simply create a page specifier inside of the 
        # page method declaration that the button is declared in, and then follow the structure of the code seen above.       

    def startup_page(self):

        self.clear_widgets() # Clear any existing widgets from the interface to start fresh

        lockbox_label = CTkLabel(self.root, text="Lockbox", font=('Arial', 30)) # Creates a label widget for the application title "Lockbox"
        lockbox_label.pack() # Add the lockbox_label to the application window using pack geometry manager, which organizes widgets in a block

        desc_label = CTkLabel(self.root, text="a password manager", font=('Arial', 15)) # Create a descriptive label widget below the application title
        desc_label.pack() # Add the desc_label to the application window below the title label

        # Create a log in button, which has a command calling login_page
        # Clicking this button will execute the login_page method, navigating to the login interface
        login_btn = CTkButton(self.root, text="Log In", command=self.login_page)
        login_btn.pack() # Add the login button to the application window, below the description label

        # Create a sign up button
        # Clicking this button executes the signup_page method, leading to the sign-up interface
        signup_btn = CTkButton(self.root, text="Sign Up", command=self.signup_page)
        signup_btn.pack() # Add the signup button to the application window, below the login button

    # Define the method for displaying the login page
    def login_page(self):
        
        self.curr_page = 'login' # Page identifier used by on_enter_press method

        self.clear_widgets() # Clear any existing widgets to prepare for displaying the login interface

        login_label = CTkLabel(self.root, text="Log In") # Creates a label widget for the login page title "Log In"
        login_label.pack() # Add the login_label to the application window using pack geometry manager

        username_entry = CTkEntry(self.root, placeholder_text="Username") # Create an entry widget and displays "Username" as placeholder text
        username_entry.pack() # Add the username entry field to the application window

        # Creates an entry widget and displays "Password" as placeholder text
        # Hides the entered text with asterisks (*) for privacy
        pw_entry = CTkEntry(self.root, placeholder_text="Password", show='*')
        pw_entry.pack() # Add the password entry field to the application window

        # Creates a button, labeled "Log In", for submitting the login information
        # The button is linked to perform_login, which attempts to authenticate the user with the entered credentials
        self.login_btn = CTkButton(self.root, text="Log In", command=lambda:self.account.perform_login(username_entry.get(), pw_entry.get()))
        self.login_btn.pack() # Add the login button to the application window

        # Creates a back button, labeled "←", for returning to the startup page 
        # The button is linked to startup_page, which takes the user back to the initial screen of the application
        back_button = CTkButton(self.root, text="←", command=self.startup_page)
        back_button.pack() # Add the back button to the application window

    # Define the method to display the sign-up page
    def signup_page(self):

        self.curr_page = 'signup' # Page identifier used by on_enter_press method

        self.clear_widgets() # Clears any existing widgets from the display

        # Create and display a label indicating this page is for user sign-up
        signup_label = CTkLabel(self.root, text="Sign Up")
        signup_label.pack()

        # Set up an entry widget for the user to input a username
        # Placeholder text "Username" is displayed when the entry is empty
        username_entry = CTkEntry(self.root, placeholder_text="Username")
        username_entry.pack()

        # Set up a password entry widget
        # The entered text is obscured (shown as '*') for privacy
        pw_entry = CTkEntry(self.root, placeholder_text="Password", show='*')
        pw_entry.pack()

        # Set up another password entry widget for password confirmation
        # This also obscures entered text and serves to verify the user typed their password correctly
        confirm_pw_entry = CTkEntry(self.root, placeholder_text="Confirm Password", show='*')
        confirm_pw_entry.pack()

        # Create a sign-up button that, when clicked, calls the perform_signup method
        # This method is presumably responsible for processing the sign-up information
        self.signup_btn = CTkButton(self.root, text="Sign Up", command=lambda:self.account.perform_signup(username_entry.get(), pw_entry.get(), confirm_pw_entry.get()))
        self.signup_btn.pack()

        # Create a back button allowing users to return to the previous page (likely the startup page)
        # This is helpful in case the user decides not to sign up or wants to return to the login page
        back_button = CTkButton(self.root, text="←", command=self.startup_page)
        back_button.pack()

    # Define the method to display the main menu options to the user
    def menu_page(self, username):
        
        self.curr_page = 'menu'

        self.clear_widgets() # Clear any existing widgets to prepare for displaying new options

        # accessing username
        un = username
        # Check if there's website data associated with the user's profile
        if not self.db.check_website_data():
            # If no website data is found, provide an option to add a new website
            # This creates a button labeled "Add New Website"
            # Clicking this button will invoke the add_website_page method, leading the user to a page
            # where they can enter details for a new website
            add_website_btn = CTkButton(self.root, text="Add New Website", command=lambda:self.add_website_page(un))
            add_website_btn.pack() # Display the button using pack geometry manager, which adds it to the application window

        # Regardless of whether website data exists, provide an option to view websites
        # This creates a view websites button 
        # Clicking this button will invoke the view_websites_page method, allowing the user to see a list
        # of websites associated with their account
        view_websites_btn = CTkButton(self.root, text="View Websites", command=lambda:self.view_websites_page(un))
        view_websites_btn.pack() # Adds view website button to application window
        # Creates the generate password button in main menu, invoking the generate_pass_page when user clicks
        pass_gen_btn = CTkButton(self.root, text="Generate New Password", command=lambda:self.generate_pass_page(un))
        pass_gen_btn.pack()

    # Define a method to display the page for adding new website information
    def add_website_page(self, username):
        
        self.curr_page = 'addwebsite'

        un = username

        self.clear_widgets() # Clear any previously displayed widgets to prepare for new content

        # Create and display a label to indicate this page is for adding new website details
        website_label = CTkLabel(self.root, text="Add New Website")
        website_label.pack()

        # Set up an entry widget for the user to input the name of the website
        website_url_entry = CTkEntry(self.root, placeholder_text="URL")
        website_url_entry.pack()

        # Set up an entry widget for the user to input their username for the website
        website_username_entry = CTkEntry(self.root, placeholder_text="Username")
        website_username_entry.pack()

        # Set up an entry widget for the user to input their password for the website
        # Entered text is obscured (shown as '*') for privacy
        website_pw_entry = CTkEntry(self.root, placeholder_text="Password", show='*')
        website_pw_entry.pack()

        # Create a button labeled "Save" that, when clicked, calls the save_website_details method
        # This method is presumably responsible for processing and storing the entered website information
        self.save_btn = CTkButton(self.root, text="Save", command=lambda:self.db.save_website_details(un, website_url_entry.get(), website_username_entry.get(), website_pw_entry.get()))
        self.save_btn.pack()

        # Create a back button that allows users to return to the main menu
        # This provides a convenient way to navigate away from the add website page without saving
        back_button = CTkButton(self.root, text="←", command=lambda:self.menu_page(un))
        back_button.pack()

    # Define the method to display the webpage credentials associated with the user
    def view_websites_page(self, username):
        
        un = username

        self.clear_widgets()

        account_id = self.db.get_user_account_id(un)
        
        if account_id is not None:
            try:
                # Establish a connection to the SQLite database named 'lockbox.db'
                con = sqlite3.connect("lockbox.db")
                # Create a cursor object to execute SQL commands
                cur = con.cursor()

                # Execute a SQL query to select website data for the provided lockbox_account_id
                cur.execute("SELECT website_name, website_username, website_password FROM websites WHERE lockbox_account_id = ?", (account_id,))
                # Fetch all rows of the query result
                self.website_data = cur.fetchall()

                # Close the database connection
                con.close()

                if self.website_data:
                    # Display website data
                    website_label = CTkLabel(self.root, text="Your Websites:")
                    website_label.pack()
                    for website in self.website_data:
                        website_name, website_username, website_password = website
                        website_info = f"Website: {website_name}, Username: {website_username}, Password: {website_password}"
                        website_info_label = CTkLabel(self.root, text=website_info)
                        website_info_label.pack()
                else:
                    # No websites found for the user
                    no_website_label = CTkLabel(self.root, text="No websites found.")
                    no_website_label.pack()

            except sqlite3.Error as e:
                # Handle any SQLite error encountered during the operation
                print("Error while retrieving website data:", e)
        else:
            # No lockbox_account_id found for the username
            print("No lockbox account found for the provided username.")

        # Add a back button to the GUI that, when clicked, will call the menu_page method
        # to return the user to the main menu
        back_button = CTkButton(self.root, text="← Back to Menu", command=lambda:self.menu_page(un))
        back_button.pack()

    #Define a method to display the page for generating a new password
    def generate_pass_page(self, username):
        
        self.curr_page = 'genpass'

        un = username

        self.clear_widgets() # Clear any existing widgets to prepare for displaying new options
        
        # Method for updating the value of the slider
        def sliding_value(value):
            slider_value_label.configure(text=f"Character Count: {int(value)}", font=('Arial Bold', 14))
        
        # Frame to hold the slider and its value label
        slider_frame = CTkFrame(self.root, fg_color="transparent")
        slider_frame.pack(pady=10)
        
        # Create the slider
        char_len_slider = CTkSlider(slider_frame,
                                from_=4,
                                to=32,
                                width=160,
                                height=16,
                                border_width=5.5,
                                command=sliding_value)
        # Initialize slider value to 8, but minimum is 4 as seen above with "from_=4"
        char_len_slider.set(8)
        
        # Label to display the slider's value, placed above the slider
        slider_value_label = CTkLabel(slider_frame, text=f"Character Count: {char_len_slider.get()}", font=('Arial Bold', 14))
        slider_value_label.pack(side='top')
        
        # Place slider
        char_len_slider.pack(side='top')
        # Label that tells the user to select one of the password checkbox options
        # in order to avoid error when trying to generate password without any characters
        user_option_warning = CTkLabel(self.root, text="Please Select at Least One of the Following", font=('Arial Bold', 15), text_color='red') 
        user_option_warning.pack()
        # Frame to hold all the checkboxes
        checkbox_frame = CTkFrame(self.root, fg_color="transparent")
        checkbox_frame.pack(pady=10) 
        #Check Boxes for including certain characters
        include_upper_box = CTkCheckBox(checkbox_frame, text="Include Uppercase Letters", font=('Arial Bold', 14))
        include_upper_box.pack(padx=10, anchor='w')
        include_lower_box = CTkCheckBox(checkbox_frame, text="Include Lowercase Letters", font=('Arial Bold', 14))
        include_lower_box.pack(padx=10, anchor='w')
        include_digit_box = CTkCheckBox(checkbox_frame, text="Include Digits", font=('Arial Bold', 14))
        include_digit_box.pack(padx=10, anchor='w')
        include_special_box = CTkCheckBox(checkbox_frame, text="Include Special Characters", font=('Arial Bold', 14))
        include_special_box.pack(padx=10, anchor='w')
        # Storing user specified values for pass generation as
        # shorter varaible names for passing to generate_pass function in accounts
        length=char_len_slider
        u=include_upper_box
        l=include_lower_box
        d=include_digit_box
        spec=include_special_box
        # Button that calls the generate_pass function, using the shortened variable names as arguments
        self.generate_pass_btn = CTkButton(self.root, text="Generate Password", command=lambda:self.account.generate_pass(un, length, u, l, d, spec))
        self.generate_pass_btn.pack()
        # Takes user back to main menu if they don't want to generate a password
        back_button = CTkButton(self.root, text="←", command=lambda:self.menu_page(un))
        back_button.pack()