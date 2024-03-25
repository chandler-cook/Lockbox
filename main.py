import customtkinter
from customtkinter import *
from account import Account
from GUI import GUI 
from DB import Database

root = CTk() # create a root customtkinter window
root.title("Lockbox") # set the title of the window
root.geometry("500x300") # set the initial size of the window

# Sets default appearance and theme of window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

gui_instance = GUI(root, None, None) # Creating an instance of the GUI class, passing the root window and None as account instance.
db_instance = Database(gui_instance, None) # Database instance, passing GUI instance

# Ensures that the database and tables are set up
gui_instance.db = db_instance
gui_instance.account = None  # Set account_instance to None for now
db_instance.gui = gui_instance
db_instance.create_tables()  # Call create_tables() before instantiating Account

# Now instantiate Account
account_instance = Account(root, gui_instance, db_instance) # Creating an instance of the Account class, passing the root window and just created gui instance
gui_instance.account = account_instance  # Update account_instance with correct reference

# Ensures that the database and tables are set up
db_instance.create_tables()

root.mainloop() # start customtkinter app