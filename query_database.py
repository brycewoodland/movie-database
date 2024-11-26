import sqlite3

# Connect to the database
conn = sqlite3.connect('C:\\Users\\bb_br\\SQLite\\movieDatabase.db')
cursor = conn.cursor()

# Query data from the movies table
cursor.execute('SELECT * FROM movies')

# Fetch all rows from the executed query
movie_rows = cursor.fetchall()

# Process and print the results
for row in movie_rows:
    print(row)

# Query data from the users table
cursor.execute('SELECT * FROM users')

# Fetch all rows from the executed query
user_rows = cursor.fetchall()

# Process and print the results
print()
for row in user_rows:
    print(row)

# Query data for the users ratings
cursor.execute('''
    SELECT movies.title, users.name, ratings.rating
    FROM ratings
    JOIN movies ON ratings.movie_id = movies.id
    JOIN users ON ratings.user_id = users.id
''')

# Fetch all rows from the executed query
rating_rows = cursor.fetchall()

# Process and print the results
print()
for row in rating_rows:
    print(row)

# Close the connection
conn.close()