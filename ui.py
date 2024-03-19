from tkinter import *
from tkinter import messagebox
from customtkinter import *

root = CTk()
root.geometry("500x300")
root.title("Lockbox")

def startup_page():
    def login_page():

        login_btn.destroy()
        signup_btn.destroy()

        startup = CTkFrame(root)
        startup.pack()

        login_label = CTkLabel(startup, text="Log In")
        login_label.pack()

        #username box
        username=CTkEntry(startup, placeholder_text="Username")
        username.pack()

        #password box
        pw = CTkEntry(startup, placeholder_text="Password", show='*')
        pw.pack()

        def back():
            lockbox_label.destroy()
            desc_label.destroy()
            login_label.destroy()
            username.destroy()
            pw.destroy()
            back_button.destroy()
            login.destroy()
            startup.destroy()
            startup_page()

        back_button = CTkButton(startup, text="←", command=back)
        back_button.pack()

        login = CTkButton(startup, text="Log In")
        login.pack()


    def signup_page():
        #removes all previous buttons
        login_btn.destroy()
        signup_btn.destroy()
    
        startup = CTkFrame(root)
        startup.pack()

        signup_label = CTkLabel(startup, text="Sign Up")
        signup_label.pack()

        #username box
        user_label = CTkLabel(startup, text="Create a username: ")
        user_label.pack()
        username=CTkEntry(startup, placeholder_text="Username")
        username.pack()

        #password and confirm password box
        pw_label = CTkLabel(startup, text="Create a password: ")
        pw = CTkEntry(startup, placeholder_text="Password", show='*')
        pw_label.pack()
        pw.pack()
        confirm_pw_label = CTkLabel(startup, text="Retype your password: ")
        confirm_pw = CTkEntry(startup, placeholder_text="Confirm Password", show='*')
        confirm_pw_label.pack()
        confirm_pw.pack()

        def back():
            lockbox_label.destroy()
            desc_label.destroy()
            signup_label.destroy()
            user_label.destroy()
            username.destroy()
            pw_label.destroy()
            pw.destroy()
            confirm_pw_label.destroy()
            confirm_pw.destroy()
            back_button.destroy()
            signup.destroy()
            startup.destroy()
            startup_page()


        back_button = CTkButton(startup, text="←", command=back)
        back_button.pack()

        signup = CTkButton(startup, text="Sign Up")
        signup.pack()

    lockbox_label=CTkLabel(root, text="Lockbox", font=('Arial', 30))
    desc_label=CTkLabel(root, text="a password manager", font=('Arial', 15))
    lockbox_label.pack()
    desc_label.pack()

    login_btn = CTkButton(root, text="Log In", command=login_page)
    login_btn.pack()

    signup_btn = CTkButton(root, text="Sign Up", command=signup_page)
    signup_btn.pack()
    
startup_page()
root.mainloop()