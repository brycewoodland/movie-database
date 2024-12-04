## Overview

**Project Title**: Movie Database Manager with OMDB Integration

**Project Description**:
A Python-based application that manages a movie database, allowing users to add, update, delete, and query movies, users, and ratings. The program integrates with the OMDb API to fetch movie details, simplifying the process of adding movies to the database. Additionally, it provides a user-friendly console interface for interaction.

**Project Goals**:
- To manage a movie database effectively with CRUD operations for movies, users, and ratings.
- To integrate with an external API (OMDb) for fetching and storing detailed movie information.
- To provide a simple interface for user interactions with the database.

## Instructions for Build and Use

Steps to build and/or run the software:

1. Install SQLite and Python
2. Install required libraries:

   `bash
    pip install sqlite3 requests python-dotenv
  `
4. Set up .env file in the project directory with your OMDb key:

   `bash
   OMDB_API_KEY=your_api_key_here
   `
5. Create the SQLite databse movieDatabase.db with the following schema:
  ```sql
     CREATE TABLE movies (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      year INTEGER NOT NULL,
      genre TEXT NOT NULL
    );
  
  CREATE TABLE users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL
  );
  
  CREATE TABLE ratings (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      movie_id INTEGER NOT NULL,
      rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
      UNIQUE(user_id, movie_id),
      FOREIGN KEY(user_id) REFERENCES users(id),
      FOREIGN KEY(movie_id) REFERENCES movies(id)
  );
  ```
6. Run the script:

   `bash
   python <script_name>.py
   `

Instructions for using the software:

1. Launch the application. You will see a menu with options for different operations.
2. Follow the prompts to add movies, users, or ratings or to update, delete, or query the database.
3. To import movies using the OMDb API, add titles to a list in the ```import_movies_from_api```function and call it.

## Development Environment 

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Python: Version 3.8 or higher
* SQLite3: Integrated with Python for database management
* Requests: For making HTTP API calls (pip install requests)
* python-dotenv: For managing environment variables (pip install python-dotenv)

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [SQLite Tutorial](https://www.sqlitetutorial.net/)
* [sqlite3 - DB-API 2.0 interface for SQLite databases](https://docs.python.org/3.8/library/sqlite3.html)
* [SQLite - Python](https://www.tutorialspoint.com/sqlite/sqlite_python.htm)
* [OMDb API](https://www.omdbapi.com/)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Improve the user interface for better user experience (e.g., use a GUI library).
* [ ] Implement functionality for exporting data to a CSV or JSON file.
* [ ] Enhance security, especially for managin user email and data integrity.
* [ ] Implement a login and logout.
