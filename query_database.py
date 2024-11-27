import sqlite3

# Connect to the database
conn = sqlite3.connect('C:\\Users\\bb_br\\movieDatabase\\movieDatabase.db')
cursor = conn.cursor()

def insert_movie():
    '''
    This function inserts a new movie into the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    title = input('Enter movie title: ')

    valid_year = False
    while not valid_year:
        try:
            year = int(input('Enter movie year: '))
            valid_year = True
        except ValueError:
            print('Invalid input. Please enter a valid year.')

    genre = input('Enter movie genre: ')
    cursor.execute('INSERT INTO movies (title, year, genre) VALUES (?, ?, ?)', (title, year, genre))
    conn.commit()
    print('Movie added successfully!')

def insert_user():
    '''
    This function inserts a new user into the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    name = input('Enter user name: ')
    email = input('Enter user email: ')
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    print('User added successfully!')

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
            user_id = int(input('Enter user ID: '))
            cursor.execute('SELECT id FROM users WHERE id = ?', (user_id))
            if cursor.fetchone() is None:
                raise ValueError('User ID does not exist.')
            
            movie_id = int(input('Enter movie ID: '))
            cursor.execute('SELECT id FROM movies WHERE id = ?', (movie_id))
            if cursor.fetchone() is None:
                raise ValueError('Movie ID does not exist.')
            
            rating = int(input('Enter rating (1-5): '))
            if rating < 1 or rating > 5:
                raise ValueError('Rating must be between 1 and 5.')
            
            valid_input = True
        except ValueError as e:
            print(f'Invalid input: {e}')
    
    try:
        cursor.execute('INSERT INTO ratings (user_id, movie_id, rating) VALUES (?, ?, ?)', (user_id, movie_id, rating))
        conn.commit()
        print('Rating added successfully!')
    except sqlite3.IntegrityError:
        print('Error: This user has already rated this movie.')

def update_movie():
    '''
    This function updates an existing movie in the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    movie_id = int(input('Enter movie ID to update: '))
    cursor.execute('SELECT id FROM movies WHERE id = ?', (movie_id))
    if cursor.fetchone() is None:
        print('Movie ID does not exist.')
        return
    
    title = input('Enter new movie title: ')
    year = int(input('Enter new movie year: '))
    genre = input('Enter new movie genre: ')
    cursor.execute('UPDATE movies SET title = ?, year = ?, genre = ? WHERE id = ?', (title, year, genre, movie_id))
    conn.commit()
    print('Movie updated succesfully!')

def update_user():
    '''
    This function updates an existing movie in the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    user_id = int(input('Enter user ID to update: '))
    cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    if cursor.fetchone() is None:
        print('User ID does not exist.')
        return
    
    name = input('Enter new user name: ')
    email = input('Enter new user email: ')
    cursor.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (name, email, user_id))
    conn.commit()
    print('User updated successfully!')

def update_rating():
    '''
    This function updates an existing movie in the database.

    Parameters:
    NONE

    Returns:
    NONE
    '''
    user_id = int(input('Enter user ID: '))
    movie_id = int(input('Enter movie ID: '))
    cursor.execute('SELECT rating FROM ratings WHERE user_id = ? AND movie_id = ?', (user_id, movie_id))
    if cursor.fetchone() is None:
        print('Rating does not exist for this user and movie.')
        return
    
    rating = int(input('Enter new rating (1-5): '))
    if rating < 1 or rating > 5:
        print('Rating must be between 1 and 5.')
        return

    cursor.execute('UPDATE ratings SET rating = ? WHERE user_id = ? AND movie_id = ?', (rating, user_id, movie_id))
    conn.commit()
    print('Rating updated successfully!')

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
    print('\nMovies:')
    for row in movie_rows:
        print(row)

    # Query data from the users table
    cursor.execute('SELECT * FROM users')
    user_rows = cursor.fetchall()
    print('\nUsers:')
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
    print('\nRatings:')
    for row in rating_rows:
        print(row)

# Main function to run the script
def main():
    while True:
        print('\nOptions:')
        print('1. Add a new movie')
        print('2. Add a new user')
        print('3. Add a new rating')
        print('4. Update a movie')
        print('5. Update a user')
        print('6. Update rating')
        print('7. Query data')
        print('8. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            insert_movie()
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
            query_data()
        elif choice == '8':
            break
        else:
            print('Invalid choice. Please try again.')

if __name__ == '__main__':
    main()
    conn.close()