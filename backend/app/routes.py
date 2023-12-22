from app import app
from app.utils import get_data, find_movies
from flask import request, jsonify

def configure_routes(app):
    @app.route('/process_ratings', methods=['POST'])
    def process_ratings():
        user_input = request.json
        data, weights = get_data()

        num_movies = user_input.get("num_movies", 5)  # Default to 5 if not provided
        user_ratings = user_input.get("ratings", {})

        recommended_movies = find_movies(data, weights, user_ratings, num_movies)
        return jsonify(recommended_movies)
