import sqlite3
import bcrypt

class Database():
    def __init__(self, gui_instance):
        self.gui = gui_instance
        self.account_id = None 

    def create_tables(self):
        
        con = sqlite3.connect("lockbox.db") # Connect to the database
        cur = con.cursor() # Create a cursor object to execute SQL commands
        
        
        # Create the lockbox_accounts table
        cur.execute('''CREATE TABLE IF NOT EXISTS lockbox_accounts (
                    lockbox_account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL)''')

        # id: website id for multiple websites
        # lockbox_account_id: id that is the same as the users id to connect user to their websites
        # website name: name of wesbite
        # website_password: password for website
        cur.execute('''CREATE TABLE IF NOT EXISTS websites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lockbox_account_id INTEGER,
                    website_name TEXT NOT NULL,
                    website_username TEXT NOT NULL,
                    website_password TEXT NOT NULL,
                    FOREIGN KEY(lockbox_account_id) REFERENCES lockbox_accounts(lockbox_account_id))''')

        # Commit changes and close connection
        con.commit()
        con.close()

    def check_user(self, username):

        un = username

        try:
            con = sqlite3.connect("lockbox.db")  # Connect to the database
            cur = con.cursor()  # Create a cursor object to execute SQL commands

            # Execute a SQL query to select the username from the 'lockbox_accounts' table
            # where the 'username' column matches the provided username
            cur.execute("SELECT username FROM lockbox_accounts WHERE username = ?", (un,))
            result = cur.fetchone()  # Fetch the first row of the results

            con.close()  # Close the database connection

            # Return True if the username exists, False otherwise
            return result is not None
        except sqlite3.Error as e:
            # Catch and print any SQLite error encountered during the operation
            print("Error while checking user:", e)
            return False  # Return False in case of error

    def insert_user(self, username, password):
        con = sqlite3.connect("lockbox.db") # Connect to the database
        cur = con.cursor() # Create a cursor object to execute SQL commands

        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the new user into the lockbox_accounts table
        cur.execute("INSERT INTO lockbox_accounts (username, password) VALUES (?, ?)", (username, hashed_password))
        con.commit()
        
        # For error checking
        print("User added successfully.")
        con.close() # Close connection
        
    def authenticate_user(self, username, password):
        
        un = username
        pw = password

        con = sqlite3.connect("lockbox.db") # Connect to the database
        cur = con.cursor() # Create a cursor object to execute SQL commands

        # uses parameterized queries correctly with the ? placeholder for the SQL parameter, 
        # and then provides the actual parameter values ((username,)) separately. This method prevents 
        # the SQL engine from executing any unintended SQL commands. (SQLi)

        # Query the database to check if the username exists
        cur.execute("SELECT password FROM lockbox_accounts WHERE username=?", (un,))
        result = cur.fetchone()

        if result:  # If username exists
            hashed_password = result[0]
            # Check if the provided password matches the hashed password
            if bcrypt.checkpw(pw.encode('utf-8'), hashed_password):
                print("Login successful!")
                cur.execute("SELECT * FROM websites WHERE lockbox_account_id=(SELECT id FROM lockbox_accounts WHERE username=?)", (un,))
                profile_data = cur.fetchall()
                con.close()

                if profile_data:  # Check if any profile data was fetched
                    return profile_data, None  # Return profile data and no error message
                else:
                    return None, "No profile data found for the user."  # Return special value indicating no profile data
        con.close()
        return None, "Invalid username or password."

    # Define a method to fetch the account ID for a given username from the database
    def get_user_account_id(self, username):
        try:
            # Establish a connection to the SQLite database named 'lockbox.db'
            con = sqlite3.connect("lockbox.db")
            # Create a cursor object to execute SQL commands
            cur = con.cursor()

            # Execute a SQL query to select the ID from the 'lockbox_accounts' table
            # where the 'username' column matches the provided username
            cur.execute("SELECT lockbox_account_id FROM lockbox_accounts WHERE username = ?", (username,))
            # Fetch the first row of the results
            result = cur.fetchone()

            # Check if a result was found
            if result:
                self.account_id = result[0]
                return self.account_id  # Return the account ID (first column of the row) if found
            else:
                return None  # Return None if there was no match for the username
        except sqlite3.Error as e:
            # Catch and print any SQLite error encountered during the operation
            print("Error while retrieving user account ID:", e)
            return None  # Return None in case of error
        finally:
            # Ensure that the database connection is closed to free resources
            if con:
                con.close()


    def insert_new_website(self, user_id, website_name, website_username, website_password):
        con = sqlite3.connect("lockbox.db")  # Connect to the database
        cur = con.cursor()  # Create a cursor object to execute SQL commands

        # Need the id to put into the DB
        user_id = self.get_user_account_id
        
        # Insert the new website into the websites table
        sql = '''INSERT INTO websites (lockbox_account_id, website_name, website_username, website_password) 
                VALUES ((SELECT lockbox_account_id FROM lockbox_accounts WHERE username=?), ?, ?, ?)'''
        values = (user_id, website_name, website_username, website_password)
        cur.execute(sql, values)
        
        # Output the inserted row
        last_inserted_id = cur.lastrowid  # Get the id of the last inserted row
        inserted_row = cur.execute("SELECT * FROM websites WHERE id = ?", (last_inserted_id,)).fetchone()
        print("Inserted Row:", inserted_row)

        con.commit()  # Commit the transaction
        con.close()   # Close the connection

    # Usage example:
    # Assuming you have an instance of your class, you can call the function like this:
    # instance.insert_new_website(username, website_name, website_username, website_password)




    # Define the method to save new website details entered by the user
    def save_website_details(self, username, website_url_entry, website_username_entry, website_pw_entry):
        
        # Giving the username a variable
        un = username
        # Retrieve the entered website name from the website name entry widget
        website_url = website_url_entry
        # Retrieve the entered username for the website from the username entry widget
        website_username = website_username_entry
        # Retrieve the entered password for the website from the password entry widget
        website_password = website_pw_entry
        
        # Need a way to get username
        
        # error checking to ensure the username is saved
        print("Before database, username: ", un)
        # Call the method to get the account ID for the current user based on their username
        # This is necessary to relate the website details with the specific user account in the database
        account_id = self.get_user_account_id(un)
        print(account_id)


        # Attempt to insert the new website details into the database
        try:
            # This method attempts to insert a new row into the database table for websites
            # It includes the current username, website name, website username, and password as parameters
            self.insert_new_website(account_id, website_url, website_username, website_password)
    
            # Displaying the data just put into the DB
            
            # WHERE lockbox_account_id = ? filters the rows based on the lockbox_account_id matching the provided account_id.
            # ORDER BY id DESC ensures that the results are ordered in descending order based on the id, so the last inserted 
            # record will be at the top.
            
            con = sqlite3.connect("lockbox.db")  # Connect to the database
            cur = con.cursor()  # Create a cursor object to execute SQL commands

            last_inserted_row = cur.execute("SELECT * FROM websites WHERE lockbox_account_id = ? ORDER BY id", (account_id,)).fetchone()
    
            con.commit()  # Commit the transaction
            con.close()   # Close the connection
    
            print(last_inserted_row)
            
            # If the insert is successful, print a confirmation message
            print("Website details saved successfully!")
        # Handle any exceptions that occur during the database insert operation
        except Exception as e:
            # If an exception occurs, show an error message with the exception details
            self.gui.show_message("error", "Failed to save website details. Error: " + str(e))

        self.gui.menu_page(username)

    # Define a method to check if website data exists for the user's account
    def check_website_data(self):
        
        con = sqlite3.connect("lockbox.db") # Establish a connection to the SQLite database named 'lockbox.db'
        cur = con.cursor() # Create a cursor object to execute SQL commands

        # Execute a SQL query to select all entries from the 'websites' table
        # where the 'lockbox_account_id' matches the user's profile ID
        cur.execute("SELECT * FROM websites WHERE lockbox_account_id = ?", (self.account_id,))
        website_data = cur.fetchall() # Fetch all rows of the query result

        con.close() # Close the database connection to free resources

        # Convert the website_data to a boolean and return it
        # This will be True if website_data contains any entries, False otherwise
        return bool(website_data)


    # Call create_tables function to ensure tables exist
    # create_tables(self)
