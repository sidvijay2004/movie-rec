import streamlit as st
import requests

def add_movies_to_watchlist(movies):
    url = 'http://localhost:5000/add_to_watchlist'
    try:
        response = requests.put(url, json={'movies': movies})
        if response.status_code == 200:
            result = response.json()
            added = result.get('added_movies', 0)
            existing = result.get('existing_movies', 0)
            errors = result.get('errors', 0)
            message = f"Added {added} new movies. {existing} movies were already in the watchlist."
            if errors > 0:
                message += f" Encountered errors with {errors} movies."
            return True, message
        else:
            return False, "Failed to add movies to watchlist"
    except requests.exceptions.RequestException as e:
        return False, f"Request failed: {e}"

def get_movie_recommendations(data):
    try:
        response = requests.post('http://localhost:5000/process_ratings', json=data)
        return response
    except requests.exceptions.RequestException as e:
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

    if st.button('Submit Ratings'):
        data = {
            'ratings': {
                'Comedy': comedy_rating,
                'Romance': romance_rating,
                'Action': action_rating,
                'Drama': drama_rating,
                'Acting Performance': acting_performance_rating,
                'Engagingness': engagingness_rating
            },
            'num_movies': 5
        }
        response = get_movie_recommendations(data)
        if response:
            st.session_state['movie_recommendations'] = response.json()
            show_movie_selection_form(st.session_state['movie_recommendations'])
        else:
            st.error("Failed to connect to Flask backend. Please check the server.")

    elif 'movie_recommendations' in st.session_state:
        show_movie_selection_form(st.session_state['movie_recommendations'])

def show_movie_selection_form(movies):
    if 'selected_movies' not in st.session_state:
        st.session_state['selected_movies'] = []

    for idx, movie in enumerate(movies):
        col1, spacer, col2, col3 = st.columns([2, 0.2, 2, 1])
        with col1:
            st.image(movie["Image URL"], width=300)
        with col2:
            expander = st.expander("Details")
            with expander:
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
        with col3:
            # checkbox_label = f"Select {movie['Title']} to Watchlist"
            checkbox_label = f"Select to Watchlist"
            if st.checkbox(checkbox_label, key=f"select_{movie['TMDBId']}"):
                if movie['TMDBId'] not in st.session_state['selected_movies']:
                    st.session_state['selected_movies'].append(movie['TMDBId'])
            else:
                if movie['TMDBId'] in st.session_state['selected_movies']:
                    st.session_state['selected_movies'].remove(movie['TMDBId'])

    if st.button("Add Selected Movies to Watchlist"):
        process_selected_movies(movies)

def process_selected_movies(movies):
    selected_movies = [movie for movie in movies if movie['TMDBId'] in st.session_state['selected_movies']]
    if selected_movies:
        movies_to_add = [{'tmdb_id': movie['TMDBId'], 'title': movie['Movie Title']} for movie in selected_movies]
        success, message = add_movies_to_watchlist(movies_to_add)
        if success:
            st.success(message)
            st.session_state['selected_movies'] = []
        else:
            st.error(message)
    else:
        st.error("No movies selected")

@st.cache_data
def fetch_movie_details(tmdb_id):
    api_key = 'b2514b23ba9a0af593911399736a265b'
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None
