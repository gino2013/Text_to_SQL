import sqlite3

# Connect to or create a SQLite database
conn = sqlite3.connect("dummy.db")

# Create a cursor
cursor = conn.cursor()

# Execute a SQL command to create a table
cursor.execute("""
CREATE TABLE Customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

# Insert sample data into the table
cursor.execute("""
INSERT INTO Customers (name, age)
VALUES
    ("John Doe", 35),
    ("Jane Doe", 32),
    ("Jim Smith", 40),
    ("Jill Smith", 38)
""")

# Commit the changes
conn.commit()

# Close the connection
conn.close()
