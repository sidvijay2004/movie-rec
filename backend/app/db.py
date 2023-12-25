import mysql.connector
from flask import request, jsonify
from . import app  # Import the Flask app instance from the backend package
from .utils import fetch_image_from_tmdb  # Adjust the import path if necessary

# app = Flask(__name__)

# Replace with your database credentials
host = 'localhost'  # or '127.0.0.1'
port = 3306
user = 'sid'
password = '$Sidtheboss1'
database = 'movie_app'

# Create a database connection
conn = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

# Create a cursor to execute SQL queries
cursor = conn.cursor()

@app.route('/test_db_connection')
def test_db_connection():
    try:
        cursor.execute("SELECT * FROM movies")
        movies_data = cursor.fetchall()
        
        # Enhance movie data with the image URL from TMDB
        enhanced_movies_data = []
        for movie in movies_data:
            # Assuming tmdb_id is the second element in the movie tuple
            tmdb_id = movie[1]
            image_url = fetch_image_from_tmdb(tmdb_id)
            movie_dict = {
                "id": movie[0],
                "tmdb_id": tmdb_id,
                "title": movie[2],
                "watched": movie[3],
                "image_url": image_url  # Add the image URL to the movie data
            }
            enhanced_movies_data.append(movie_dict)

        return jsonify({"message": "Database connection successful", "data": enhanced_movies_data})
    except Exception as e:
        return jsonify({"message": f"Database connection error: {str(e)}"})

        
@app.route('/add_to_watchlist', methods=['PUT'])
def add_to_watchlist():
    print("reached DB Connection")
    data = request.get_json()
    movies = data['movies']

    added_movies = 0
    existing_movies = 0
    errors = 0

    for movie in movies:
        tmdb_id = movie['tmdb_id']
        title = movie['title']

        try:
            cursor.execute("SELECT COUNT(*) FROM movies WHERE tmdb_id = %s", (tmdb_id,))
            count = cursor.fetchone()[0]

            if count == 0:
                query = "INSERT INTO movies (tmdb_id, title, watched) VALUES (%s, %s, 0)"
                cursor.execute(query, (tmdb_id, title))
                added_movies += 1
            else:
                existing_movies += 1
        except mysql.connector.Error:
            errors += 1

    if added_movies > 0:
        conn.commit()

    response_message = {
        'added_movies': added_movies,
        'existing_movies': existing_movies,
        'errors': errors
    }
    return jsonify(response_message), 200 if added_movies > 0 or existing_movies > 0 else 500

