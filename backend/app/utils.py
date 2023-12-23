import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import requests


def get_data():
    # Load the CSV file into a DataFrame
    file_path = 'data/movie_dataset.csv'  # Adjust this path as necessary if your folder is named 'data'
    data = pd.read_csv(file_path)

    # Define the weights for the features (currently unused)
    # weights = {'Comedy': 1.5, 'Romance': 1, 'Drama': 2, 'Action': 1, 'Acting Performance': 1.5, 'Engagingness': 1}
    return data  # , weights

def find_movies(data, user_ratings, num_movies):
    # Extract features
    feature_columns = ['Comedy', 'Romance', 'Drama', 'Action', 'Acting Performance', 'Engagingness']
    features = data[feature_columns].copy()

    # # Apply weights to features (currently not applied)
    # for column, weight in weights.items():
    #     features[column] *= weight

    # Scale the features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Creating a KNN model and fitting it
    knn_model = NearestNeighbors(n_neighbors=num_movies, algorithm='auto')
    knn_model.fit(scaled_features)

    # Convert user ratings into a format suitable for scaling
    user_ratings_list = [user_ratings.get(cat, 0) for cat in feature_columns]
    user_ratings_scaled = scaler.transform([user_ratings_list])
    print("Scaled user ratings:", user_ratings_scaled)  # Log scaled ratings

    distances, indices = knn_model.kneighbors(user_ratings_scaled)
    print("Recommended movie indices:", indices)  # Log recommended indices

    # Fetch movie recommendations
    movies_info = []
    for idx in indices[0]:
        movie_data = data.iloc[idx]
        tmdb_id = movie_data['TMDBId']  # Adjusted to use 'TMDBId'
        image_url = fetch_image_from_tmdb(tmdb_id)  # Function to fetch image URL
        movie_info = {
            'Movie Title': movie_data['Movie Title'],
            'Image URL': image_url,
            'TMDBId': tmdb_id  # Include the TMDB ID here
        }
        movies_info.append(movie_info)

    return movies_info

def fetch_image_from_tmdb(tmdb_id):
    api_key = 'b2514b23ba9a0af593911399736a265b'
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/images?api_key={api_key}&include_image_language=en"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            image_path = data['backdrops'][0]['file_path'] if data['backdrops'] else None
            image_url = f"https://image.tmdb.org/t/p/original{image_path}" if image_path else None
            return image_url
        else:
            print(f"TMDB API error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching image from TMDB: {e}")
        return None

