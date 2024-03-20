import sqlite3
import bcrypt

def create_tables():
    # Connect to the database
    con = sqlite3.connect("lockbox.db")
    cur = con.cursor()

    # Create lockbox_accounts table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS lockbox_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    # Create websites table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS websites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lockbox_account_id INTEGER NOT NULL,
        website_name TEXT NOT NULL,
        website_username TEXT NOT NULL,
        website_password TEXT NOT NULL,
        FOREIGN KEY (lockbox_account_id) REFERENCES lockbox_accounts(id)
    )''')

    # Commit changes and close connection
    con.commit()
    con.close()

def insert_new_user(username, password):
    # Connect to the database
    con = sqlite3.connect("lockbox.db")
    cur = con.cursor()

    # Hash the password before storing it in the database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert the new user into the lockbox_accounts table
    cur.execute("INSERT INTO lockbox_accounts (username, password) VALUES (?, ?)", (username, hashed_password))
    con.commit()

    # Close connection
    con.close()

def authenticate_user(username, password):
    # Connect to the database
    con = sqlite3.connect("lockbox.db")
    cur = con.cursor()



# uses parameterized queries correctly with the ? placeholder for the SQL parameter, 
# and then provides the actual parameter values ((username,)) separately. This method prevents 
# the SQL engine from executing any unintended SQL commands. (SQLi)

    # Query the database to check if the username exists
    cur.execute("SELECT password FROM lockbox_accounts WHERE username=?", (username,))
    result = cur.fetchone()

    if result:  # If username exists
        hashed_password = result[0]
        # Check if the provided password matches the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            print("Login successful!")
            cur.execute("SELECT * FROM websites WHERE lockbox_account_id=(SELECT id FROM lockbox_accounts WHERE username=?)", (username,))
            profile_data = cur.fetchall()
            con.close()

            if profile_data:  # Check if any profile data was fetched
                return profile_data, None  # Return profile data and no error message
            else:
                return None, "No profile data found for the user."  # Return special value indicating no profile data
    con.close()
    return None, "Invalid username or password."


def insert_new_website(username, website_name, website_username, website_password):
    # Connect to the database
    con = sqlite3.connect("lockbox.db")
    cur = con.cursor()

    # Insert the new website into the websites table
    cur.execute("INSERT INTO websites (lockbox_account_id, website_name, website_username, website_password) VALUES ((SELECT id FROM lockbox_accounts WHERE username=?), ?, ?, ?)", (username, website_name, website_username, website_password))
    con.commit()

    # Close connection
    con.close()

# Call create_tables function to ensure tables exist
create_tables()
