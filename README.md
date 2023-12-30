# Movie Recommendation System

## Overview
This application is a machine learning-based movie recommendation system that allows users to specify their preferences for various movie attributes such as comedy, romance, action, drama, acting performance, and engagement. The system suggests movies that align closely with the user's tastes. It features language and content rating filters, and also includes a watchlist for tracking movies to watch and those already watched, with the additional functionality to discover similar movies.


### Machine Learning Model Details
The core of the recommendation engine is built using the KNN algorithm, which is part of the scikit-learn library—a robust and widely-used Python library for machine learning. The KNN algorithm works by finding the 'nearest' data points in the feature space to a given input point. In the context of this movie recommendation system, the 'points' are movies, and their 'location' in feature space is determined by their attributes, such as genre balance, acting quality, and overall engagement.

Here's a brief rundown of how the ML model operates:

1. **Data Preprocessing**: The system starts by loading the movie dataset using `pandas`, a powerful data manipulation library. It ensures that the data is clean and structured appropriately for the model.

2. **Feature Scaling**: To make sure that all the movie attributes contribute equally to the recommendation process, the system scales the feature data using `StandardScaler` from scikit-learn. This step standardizes the range of the continuous initial variables so that the KNN algorithm can compute distances consistently across all dimensions of the feature space.

3. **Model Training**: Using the `NearestNeighbors` class from scikit-learn, the system trains the KNN model on the dataset. This model is now ready to infer recommendations based on the proximity of user preferences to the attributes of available movies.

4. **Recommendation Inference**: When users input their preferences, these preferences are transformed into a point in the feature space. The KNN model then identifies the nearest movie points to this user preference point—i.e., the movies most similar to the user's tastes—and suggests them as recommendations.


## Data File Explanation

### Dataset Overview
The movie recommendation system relies on a comprehensive dataset stored in a CSV file located in the `data` folder from the root directory of the project. This dataset is crucial for training the machine learning model and generating personalized movie recommendations.

### Data Structure
The dataset is structured as a CSV (Comma-Separated Values) file, which includes key attributes for a variety of movies. Each row in the file represents a unique movie, and the columns contain the following information:

- `Movie Title`: The title of the movie along with its release year.
- `TMDBId`: The unique identifier for the movie from The Movie Database (TMDB).
- `Comedy`: A numeric rating representing the movie's emphasis on comedy (scale: 1-10).
- `Romance`: A numeric rating for the movie's focus on romantic elements (scale: 1-10).
- `Drama`: A numeric rating indicating the extent of dramatic content (scale: 1-10).
- `Action`: A numeric rating for the level of action in the movie (scale: 1-10).
- `Acting Performance`: A rating assessing the quality of acting in the movie (scale: 1-10).
- `Engagingness`: A rating of how engaging or captivating the movie is (scale: 1-10).
- `Language`: The primary language of the movie.
- `Appropriateness`: A categorization of the movie's audience as either 'Adult' or 'For Everyone'.

### Sample Data
Here's a snippet from the dataset to illustrate its format:

```plaintext
Movie Title,TMDBId,Comedy,Romance,Drama,Action,Acting Performance,Engagingness,Language,Appropriateness
The Shawshank Redemption (1994),278,2,1,10,3,10,10,English,Adult
The Godfather (1972),238,2,3,10,4,10,9,English,Adult
The Godfather: Part II (1974),240,2,3,10,4,10,9,English,Adult
```

### Usage in the ML Model
The machine learning model utilizes this dataset to understand the characteristics of various movies. When a user inputs their preferences for different movie attributes, the model compares these preferences with the dataset to find movies with similar profiles. This approach allows the system to suggest movies that closely align with the user's tastes, leveraging the detailed information provided in each column of the dataset.

## Architecture

![Architecture Diagram](Code%20Architecture%20Diagram.png)

The project follows a three-tier architecture:
- **Frontend**: Developed with Streamlit for an interactive UI.
- **Backend**: Flask is used to create the RESTful API that serves the recommendation logic.
- **Database**: MySQL stores user data and watchlist information.

The file structure is as follows:

```plaintext
MOVIE-REC
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── routes.py
│   │   └── utils.py
│   └── data
│       └── movie_dataset.csv
├── frontend
│   ├── movie_recommendations.py
│   └── streamlit_app.py
├── images
│   └── no_image_found.png
├── app.py
├── Movie Rec ML.ipynb
└── README.md
```

## Installation Guide

### Prerequisites
- Python 3.8+
- MySQL Server
- TMDB API Key

### Setup and Installation

1. Clone the repository:
  ```
  git clone [<repository-url>](https://github.com/sidvijay2004/movie-rec.git)
  ```
  ```
  cd movie-rec
  ```

2. Install dependencies:
  ```
  pip install -r requirements.txt
  ```

3. Configure MySQL Database:
- [Download and install MySQL](https://dev.mysql.com/downloads/mysql/)
- Create a MySQL database and user.
- Update the `backend/app/db.py` with your database credentials:
  ```python
  host = 'example_db_host'
  port = 3306
  user = 'example_user'
  password = 'example_password'
  database = 'example_database'
  ```

4. Add your TMDB API Key:
- [Obtain a TMDB API key](https://developers.themoviedb.org/3/getting-started/introduction)
- Open `frontend/movie_recommendations.py`
- Open `backend/app/utils.py`
- Replace the placeholder with your TMDB API key at the top of these files.


### Running the Application

1. Start the Flask backend:
  ```
  python app.py
  ```

2. Launch the Streamlit frontend:
- Navigate to the `frontend` directory by running:
    ```
    cd .\frontend\
    ```
- Run:
  ```
  streamlit run streamlit_app.py
  ```

## Usage
- Input your movie preferences in the Streamlit UI.
- Apply language and content rating filters as needed.
- Manage your watchlist and explore movie recommendations.

## Contribution
Feel free to fork this repository, make improvements, and submit pull requests.

## License
This project is open-sourced under the MIT license.

## Acknowledgements
Special thanks to The Movie Database (TMDB) for the API used to fetch movie information.
