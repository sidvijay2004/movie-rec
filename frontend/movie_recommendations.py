import streamlit as st
import requests
import os


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
    st.title("Movie Recommendation Generator")
    st.markdown("<h5 style='text-align: center; color: black;'>Customize your movie recommendations!</h3>", unsafe_allow_html=True)

    # Filters Section with titles
    st.subheader("Filters")
    col1, col2 = st.columns(2)
    
    with col1:
        # st.write("Language")
        st.markdown("#### **Language**")

        # Creating checkboxes for Language within a column
        english = st.checkbox("English", value=True)
        tamil = st.checkbox("Tamil")

    with col2:
        # st.write("Audience Rating")
        st.markdown("#### **Content Rating**")

        # Creating checkboxes for Audience Rating within a column
        for_everyone = st.checkbox("For Everyone")
        adult_only = st.checkbox("Adult Only")

    # Creating sliders for each category below the filters
    st.subheader("Rate your preferred levels for each category:")
    comedy_rating = st.slider("Comedy", 1, 10, 5)
    romance_rating = st.slider("Romance", 1, 10, 5)
    action_rating = st.slider("Action", 1, 10, 5)
    drama_rating = st.slider("Drama", 1, 10, 5)
    acting_performance_rating = st.slider("Acting Performance", 1, 10, 5)
    engagingness_rating = st.slider("Engagement", 1, 10, 5)

    # Process the selected filters
    languages = []
    if english:
        languages.append("English")
    if tamil:
        languages.append("Tamil")
    audience_rating = []
    if for_everyone:
        audience_rating.append("For Everyone")
    if adult_only:
        audience_rating.append("Adult Only")

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
            'languages': languages,
            'ratings_filter': audience_rating,
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
    if not movies:  # Check if the movies list is empty
        st.write("No movie recommendations available with the given criteria.")
        return

    if 'selected_movies' not in st.session_state:
        st.session_state['selected_movies'] = []

    # Define the path to the placeholder image
    placeholder_image_path = os.path.join(os.path.dirname(__file__), "..", "images", "no_image_found.png")

    for idx, movie in enumerate(movies):
        col1, spacer, col2, col3 = st.columns([2, 0.2, 2, 1])
        with col1:
            if movie.get("Image URL"):
                st.image(movie["Image URL"], width=300)
            else:
                # Display a placeholder image
                st.image(placeholder_image_path, width=300)
        with col2:
            expander = st.expander("Details")
            with expander:
                movie_details = fetch_movie_details(movie['TMDBId'])
                if movie_details:
                    st.write("Title:", movie_details.get('title', 'N/A'))
                    st.write("Budget:", f"${movie_details.get('budget', 0):,}")
                    st.write("Revenue:", f"${movie_details.get('revenue', 0):,}")
                    st.write("Release Date:", movie_details.get('release_date', 'N/A'))
                    st.write("Tagline:", movie_details.get('tagline', 'N/A'))
                    st.write("Overview:", movie_details.get('overview', 'N/A'))
                else:
                    st.error("Failed to fetch movie details.")
        with col3:
            checkbox_label = "Select to Watchlist"
            if st.checkbox(checkbox_label, key=f"select_{movie['TMDBId']}"):
                if movie['TMDBId'] not in st.session_state['selected_movies']:
                    st.session_state['selected_movies'].append(movie['TMDBId'])
            else:
                if movie['TMDBId'] in st.session_state['selected_movies']:
                    st.session_state['selected_movies'].remove(movie['TMDBId'])

    # Align the "Add to Watchlist" button to the center or right
    _, col_button, _ = st.columns([1, 2, 1])
    with col_button:
        if st.button("Add Selected Movies to Watchlist", key='add_watchlist_button'):
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
