import sqlite3
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('OMDB_API_KEY')

# Connect to the database
conn = sqlite3.connect('C:\\Users\\bb_br\\movieDatabase\\movieDatabase.db')
cursor = conn.cursor()

# Function to fetch movie details from OMDb API using title
def fetch_movie_details(title):
    '''
    This function fetches movie details from the OMDb API using the movie title.

    Parameters:
    title (str): The title of the movie to fetch details for.

    Returns:
    dict: A dictionary containing movie details if the request is successful.
    None: If the request fails or the movie is not found.
    '''
    print(f"Using API :key {api_key}")  # Debugging: Print the API key
    url = f'https://www.omdbapi.com/?t={title}&apikey={api_key}'
    print(f"Fetching details for: {title}")
    response = requests.get(url)
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")
    if response.status_code == 200:
        return response.json()
    else:
        print('Error fetching movie details')
        return None

# Function to insert a new movie
def insert_movie(title, year, genre):
    '''
    This function inserts a new movie into the database.

    Parameters:
    title (str): The title of the movie.
    year (int): The release year of the movie.
    genre (str): The genre of the movie.

    Returns:
    NONE
    '''
    cursor.execute('INSERT INTO movies (title, year, genre) VALUES (?, ?, ?)', (title, year, genre))
    conn.commit()
    print(f'Movie "{title}" added successfully!')

def insert_movie_manually():
    '''
    This function inserts a new movie into the database.

    Parameters:
    title (str): The title of the movie.
    year (int): The release year of the movie.
    genre (str): The genre of the movie.

    Returns:
    NONE
    '''
    title = input('Enter title of movie: ')
    year = int(input('Enter the release year for movie: '))
    genre = input('Enter the genre of the movie: ')
    cursor.execute('INSERT INTO movies (title, year, genre) VALUES (?, ?, ?)', (title, year, genre))
    conn.commit()
    print(f'Movie "{title}" added successfully!')


# Function to import movies from a list of titles
def import_movies_from_api(movie_titles):
    '''
    This function imports movies from a list of titles using the OMDb API.

    Parameters:
    movie_titles (list): A list of movie titles to import.

    Returns:
    NONE
    '''
    for title in movie_titles:
        movie_details = fetch_movie_details(title)
        if movie_details and movie_details['Response'] == 'True':
            year = int(movie_details['Year'])
            genre = movie_details['Genre']
            insert_movie(title, year, genre)
        else:
            print(f'Movie "{title}" not found or error occurred.')

# # List of movie titles to import
# movie_titles = [
#     'Big Jake',
# ]

# # Import movies from the list
# import_movies_from_api(movie_titles)

# Function to insert a new user
def insert_user():
    '''
    This function inserts a new user into the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    name = input("Enter user name: ")
    email = input("Enter user email: ")
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    print("User added successfully!")

# Function to insert a new rating
def insert_rating():
    '''
    This function inserts a new rating into the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    valid_input = False
    while not valid_input:
        try:
            user_id = int(input("Enter user ID: "))
            cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
            if cursor.fetchone() is None:
                raise ValueError("User ID does not exist.")
            
            movie_id = int(input("Enter movie ID: "))
            cursor.execute('SELECT id FROM movies WHERE id = ?', (movie_id,))
            if cursor.fetchone() is None:
                raise ValueError("Movie ID does not exist.")
            
            rating = int(input("Enter rating (1-5): "))
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5.")
            
            valid_input = True
        except ValueError as e:
            print(f"Invalid input: {e}")
    
    try:
        cursor.execute('INSERT INTO ratings (user_id, movie_id, rating) VALUES (?, ?, ?)', (user_id, movie_id, rating))
        conn.commit()
        print("Rating added successfully!")
    except sqlite3.IntegrityError:
        print("Error: This user has already rated this movie.")

# Function to update a movie
def update_movie():
    '''
    This function updates an existing movie in the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    movie_id = int(input("Enter movie ID to update: "))
    cursor.execute('SELECT id FROM movies WHERE id = ?', (movie_id,))
    if cursor.fetchone() is None:
        print("Movie ID does not exist.")
        return

    title = input('Enter new movie title: ')
    year = int(input('Enter new movie year: '))
    genre = input('Enter new movie genre: ')
    cursor.execute('UPDATE movies SET title = ?, year = ?, genre = ? WHERE id = ?', (title, year, genre, movie_id))
    conn.commit()
    print('Movie updated successfully!')

# Function to update a user
def update_user():
    '''
    This function updates an existing user in the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    user_id = int(input("Enter user ID to update: "))
    cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    if cursor.fetchone() is None:
        print("User ID does not exist.")
        return

    name = input("Enter new user name: ")
    email = input("Enter new user email: ")
    cursor.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (name, email, user_id))
    conn.commit()
    print("User updated successfully!")

# Function to update a rating
def update_rating():
    '''
    This function updates an existing rating in the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    user_id = int(input("Enter user ID: "))
    movie_id = int(input("Enter movie ID: "))
    cursor.execute('SELECT rating FROM ratings WHERE user_id = ? AND movie_id = ?', (user_id, movie_id))
    if cursor.fetchone() is None:
        print("Rating does not exist for this user and movie.")
        return

    rating = int(input("Enter new rating (1-5): "))
    if rating < 1 or rating > 5:
        print("Rating must be between 1 and 5.")
        return

    cursor.execute('UPDATE ratings SET rating = ? WHERE user_id = ? AND movie_id = ?', (rating, user_id, movie_id))
    conn.commit()
    print("Rating updated successfully!")

# Function to delete a movie
def delete_movie():
    '''
    This function deletes a movie from the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    movie_id = int(input("Enter movie ID to delete: "))
    cursor.execute('SELECT id FROM movies WHERE id = ?', (movie_id,))
    if cursor.fetchone() is None:
        print("Movie ID does not exist.")
        return

    cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
    conn.commit()
    print("Movie deleted successfully!")

# Function to delete a user
def delete_user():
    '''
    This function deletes a user from the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    user_id = int(input("Enter user ID to delete: "))
    cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    if cursor.fetchone() is None:
        print("User ID does not exist.")
        return

    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    print("User deleted successfully!")

# Function to delete a rating
def delete_rating():
    '''
    This function deletes a rating from the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    user_id = int(input("Enter user ID: "))
    movie_id = int(input("Enter movie ID: "))
    cursor.execute('SELECT rating FROM ratings WHERE user_id = ? AND movie_id = ?', (user_id, movie_id))
    if cursor.fetchone() is None:
        print("Rating does not exist for this user and movie.")
        return

    cursor.execute('DELETE FROM ratings WHERE user_id = ? AND movie_id = ?', (user_id, movie_id))
    conn.commit()
    print("Rating deleted successfully!")

# Function to query and print data
def query_data():
    '''
    This function queries and prints data from the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    # Query data from the movies table
    cursor.execute('SELECT * FROM movies')
    movie_rows = cursor.fetchall()
    print("\nMovies:")
    for row in movie_rows:
        print(row)

    # Query data from the users table
    cursor.execute('SELECT * FROM users')
    user_rows = cursor.fetchall()
    print("\nUsers:")
    for row in user_rows:
        print(row)

    # Query data for the users ratings
    cursor.execute('''
        SELECT movies.title, users.name, ratings.rating
        FROM ratings
        JOIN movies ON ratings.movie_id = movies.id
        JOIN users ON ratings.user_id = users.id
    ''')
    rating_rows = cursor.fetchall()
    print("\nRatings:")
    for row in rating_rows:
        print(row)

# Main function to run the script
def main():
    '''
    This function provides a menu for the user to interact with the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    while True:
        print("\nOptions:")
        print("1. Add a new movie")
        print("2. Add a new user")
        print("3. Add a new rating")
        print("4. Update a movie")
        print("5. Update a user")
        print("6. Update a rating")
        print("7. Delete a movie")
        print("8. Delete a user")
        print("9. Delete a rating")
        print("10. Query data")
        print("11. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            insert_movie_manually()
        elif choice == '2':
            insert_user()
        elif choice == '3':
            insert_rating()
        elif choice == '4':
            update_movie()
        elif choice == '5':
            update_user()
        elif choice == '6':
            update_rating()
        elif choice == '7':
            delete_movie()
        elif choice == '8':
            delete_user()
        elif choice == '9':
            delete_rating()
        elif choice == '10':
            query_data()
        elif choice == '11':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    conn.close()