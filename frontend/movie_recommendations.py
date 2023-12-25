import streamlit as st
import requests

def get_movie_recommendations(data):
    # Sending data to Flask and getting response
    print("Data sent to backend:", data)
    try:
        response = requests.post('http://localhost:5000/process_ratings', json=data)
        return response
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

def show_movie_recommendations():
    st.title("Movie Rating System")

    # Creating sliders for each category
    comedy_rating = st.slider("Comedy", 1, 10, 5)
    romance_rating = st.slider("Romance", 1, 10, 5)
    action_rating = st.slider("Action", 1, 10, 5)
    drama_rating = st.slider("Drama", 1, 10, 5)
    acting_performance_rating = st.slider("Acting Performance", 1, 10, 5)
    engagingness_rating = st.slider("Engagingness", 1, 10, 5)

    # Initialize response to None
    response = None

    # Submit button
    if st.button('Submit Ratings'):
        # Prepare data to be sent to Flask
        data = {
            'ratings': {
                'Comedy': comedy_rating,
                'Romance': romance_rating,
                'Action': action_rating,
                'Drama': drama_rating,
                'Acting Performance': acting_performance_rating,
                'Engagingness': engagingness_rating
            },
            'num_movies': 5  # Or however many movies you want to get back from the backend
        }

        # Get movie recommendations
        response = get_movie_recommendations(data)

        if response:
            print("Data received from Flask:", response.json())
        else:
            st.error("Failed to connect to Flask backend. Please check the server.")

    if response and response.status_code == 200:
        results = response.json()
        st.write("Movie Recommendations:")
        for idx, movie in enumerate(results):
            col1, col2 = st.columns([2, 2])
            with col1:
                st.image(movie["Image URL"], width=300)
            with col2:
                expander = st.expander("Details")
                with expander:
                    # Call the function to display movie details directly, without checking session state
                    movie_details = fetch_movie_details(movie['TMDBId'])
                    if movie_details:
                        st.write("Title:", movie_details['title'])
                        st.write("Budget:", f"${movie_details['budget']:,}")
                        st.write("Revenue:", f"${movie_details['revenue']:,}")
                        st.write("Release Date:", movie_details['release_date'])
                        st.write("Tagline:", movie_details['tagline'])
                        st.write("Overview:", movie_details['overview'])
                    else:
                        st.error("Failed to fetch movie details.")

@st.cache_data
def fetch_movie_details(tmdb_id):
    api_key = 'b2514b23ba9a0af593911399736a265b'
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch movie details: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception when fetching movie details: {e}")
        return None
