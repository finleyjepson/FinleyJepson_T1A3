import sqlite3

# Connect to database
conn = sqlite3.connect('credentials.db')

# Create a cursor
cur = conn.cursor()

# Create a table
cur.execute("""CREATE TABLE IF NOT EXISTS credentials (
    id integer PRIMARY KEY,
    username text,
    password text, 
    firstname text,
    lastname text,
    email text,
    phone text
)""")
conn.commit()

# Close connection
cur.close()
conn.close()