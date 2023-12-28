from . import app
from .utils import get_data, find_movies
from flask import request, jsonify
import numpy as np


@app.route('/process_ratings', methods=['POST'])
def process_ratings():
    user_input = request.json
    print("Received input:", user_input)

    # Get language and rating filters from the user input
    language_filters = user_input.get('languages', [])
    rating_filters = user_input.get('audience_rating', [])

    # Retrieve data with filters applied
    data = get_data(language_filters, rating_filters)

    num_movies = user_input.get("num_movies", 5)  # Default to 5 if not provided
    user_ratings = user_input.get("ratings", {})

    # recommended_movies = find_movies(data, weights, user_ratings, num_movies)
    recommended_movies = find_movies(data, user_ratings, num_movies)

    recommended_movies_serializable = []
    for movie in recommended_movies:
        movie_serializable = {key: (int(value) if isinstance(value, np.int64) else value)
                              for key, value in movie.items()}
        recommended_movies_serializable.append(movie_serializable)

    return jsonify(recommended_movies_serializable)
