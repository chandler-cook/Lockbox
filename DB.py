import sqlite3
import bcrypt


"""""
INSERT INTO users (name, age): 
This part specifies the table name (users) and the columns (name and age) into which data will be inserted.

VALUES (?, ?): 
This part specifies the values to be inserted into the specified columns. The ? placeholders are parameter markers used for parameterized queries to prevent SQL injection attacks and ensure data integrity.

('Gabriel Adams', 'BigDaddy@gmail.com', '1234'): 
These are tuples containing the actual values to be inserted into the respective columns. In the first INSERT statement, 'Alice' will be inserted into the name column and 30 will be inserted into the age column. In the second INSERT statement, 'Bob' will be inserted into the name column and 25 will be inserted into the age column.

By using parameterized queries (VALUES (?, ?, ?)), you separate the SQL query from the data. THIS HELPS PREVENT SQL INJECTION ATTACKS because the parameters are passed separately from the SQL query, making it impossible for an attacker to inject malicious SQL code into the query. Additionally, it ensures data integrity and proper handling of special characters in the data.
"""""
# Making connection to lockbox.db database
con = sqlite3.connect("lockbox.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS lockbox_accounts (
    username TEXT,
    email TEXT,
    password TEXT
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS profiles (
    website TEXT,
    email TEXT,
    username TEXT,
    password TEXT
)''')

# Adding an instance in the database lockbox_accounts
cur.execute("INSERT INTO lockbox_accounts (username, email, password) VALUES (?, ?, ?)", ('Gabriel Adams', 'BigDaddy@gmail.com', '1234'))

# Deleting a row from the database lockbox_accounts
cur.execute("DELETE FROM lockbox_accounts WHERE username = ? AND email = ? AND password = ?", ('Gabriel Adams', 'BigDaddy@gmail.com', '1234'))

# Save (commit) the changes
con.commit()

# Retrieve data from the table
cur.execute("SELECT * FROM lockbox_accounts")
rows = cur.fetchall()
for row in rows:
    print(row)

# Close the cursor and the connection
cur.close()
con.close()
