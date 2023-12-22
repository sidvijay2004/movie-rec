import pandas as pd
from sklearn.neighbors import NearestNeighbors

def get_data():
    # Load the CSV file into a DataFrame
    file_path = 'data/movie_dataset.csv'  # Adjust this path as necessary if your folder is named 'data'
    data = pd.read_csv(file_path)

    # Define the weights for the features
    weights = {'Comedy': 1.5, 'Romance': 1, 'Drama': 2, 'Action': 1, 'Acting Performance': 1.5, 'Engagingness': 1}
    return data, weights

def find_movies(data, weights, user_ratings, num_movies):
    # Apply weights to the features
    weighted_features = data[list(weights.keys())].copy()
    for column, weight in weights.items():
        weighted_features[column] *= weight

    # Creating a KNN model and fitting it
    knn_model = NearestNeighbors(n_neighbors=5, algorithm='auto')
    knn_model.fit(weighted_features)

    # Preparing user ratings and finding nearest neighbors
    user_ratings_weighted = [user_ratings.get(cat, 0) * weights[cat] for cat in weights]
    distances, indices = knn_model.kneighbors([user_ratings_weighted])

    # Compile the movies data based on indices
    movies_info = []
    for idx in indices[0][:num_movies]:
        movie_data = data.iloc[idx]
        movie_info = {'Movie Title': movie_data['Movie Title']}
        movie_info.update({column: movie_data[column] for column in weights.keys()})
        movies_info.append(movie_info)

    return movies_info
