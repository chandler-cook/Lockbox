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

db_instance = Database(gui_instance) # Database instance, passing GUI instance

account_instance = Account(root, gui_instance, db_instance) # Creating an instance of the Account class, passing the root window and just created gui instance

# Update instances with correct references
gui_instance.db = db_instance
gui_instance.account = account_instance
account_instance.gui = gui_instance
db_instance.gui = gui_instance  # Ensure the database has a reference to the GUI

# You could call this function at the start of your program to ensure the database and tables are set up
db_instance.create_tables()

#start app
root.mainloop() # start customtkinter app