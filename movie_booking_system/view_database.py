import sqlite3

# Connect to the database
connection = sqlite3.connect('movie_booking.db')
cursor = connection.cursor()

# Query the tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])

# Query data from a specific table (e.g., 'movie')
print("\nData in the 'movie' table:")
cursor.execute("SELECT * FROM movie;")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
connection.close()
