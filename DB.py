import sqlite3
import bcrypt

def create_tables():
    # Connect to the database
    con = sqlite3.connect("lockbox.db")
    cur = con.cursor()

    # Create lockbox_accounts table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS lockbox_accounts (
        username TEXT PRIMARY KEY,
        password TEXT
    )''')

    # Create profiles table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS profiles (
        username TEXT,
        website TEXT,
        email TEXT,
        password TEXT,
        FOREIGN KEY (username) REFERENCES lockbox_accounts(username),
        PRIMARY KEY (username, website)
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

    # Query the database to check if the username exists
    cur.execute("SELECT password FROM lockbox_accounts WHERE username=?", (username,))
    result = cur.fetchone()

    if result:  # If username exists
        hashed_password = result[0]
        # Check if the provided password matches the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            print("Login successful!")
            cur.execute("SELECT * FROM profiles WHERE username=?", (username,))
            profile_data = cur.fetchall()
            con.close()
    
            if profile_data:  # Check if any profile data was fetched
                return profile_data, None  # Return profile data and no error message
            else:
                return [], "No profile data found for the user."  # Return an empty profile_data list
        else:
            return None, "Incorrect password!"
    else:
        return None, "Username does not exist!"
    con.close()

def insert_new_profile(username, website, email, password):
    # Connect to the database
    con = sqlite3.connect("lockbox.db")
    cur = con.cursor()

    # Insert the new profile into the profiles table
    cur.execute("INSERT INTO profiles (username, website, email, password) VALUES (?, ?, ?, ?)", (username, website, email, password))
    con.commit()

    # Create a new table for the profile (if not exists)
    # This table will store website-specific username and password
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {website}_profile (
                        username TEXT,
                        password TEXT,
                        FOREIGN KEY (username) REFERENCES lockbox_accounts(username),
                        PRIMARY KEY (username, password)
                    )''')
    # Insert username and password for the website into the corresponding profile table
    cur.execute(f"INSERT INTO {website}_profile (username, password) VALUES (?, ?)", (username, password))
    con.commit()

    # Close connection
    con.close()

# Call create_tables function to ensure tables exist
create_tables()
