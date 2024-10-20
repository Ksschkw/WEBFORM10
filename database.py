import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('form_data.db')
c = conn.cursor()

# Create the table to store form data
c.execute('''CREATE TABLE IF NOT EXISTS form_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                dob TEXT NOT NULL,
                address TEXT,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip TEXT,
                phone TEXT
            )''')

# Commit and close connection
conn.commit()
conn.close()