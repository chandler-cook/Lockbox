import customtkinter
from customtkinter import *
from account import Account
from gui import GUI 
from db import Database

root = CTk() # create a root customtkinter window
root.title("Lockbox") # set the title of the window
root.geometry("500x300") # set the initial size of the window

# Sets default appearance and theme of window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

db_instance = Database()
gui_instance = GUI(root, None, db_instance) # Creating an instance of the GUI class, passing the root window and None as account instance.
account_instance = Account(root, gui_instance, db_instance) # Creating an instance of the Account class, passing the root window and just created gui instance

account_instance.gui = gui_instance # Update account_instance with gui_instance
gui_instance.account = account_instance # Update gui_instance with account_instance

root.mainloop() # start customtkinter app