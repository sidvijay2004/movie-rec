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

def main():
    st.title("Movie Rating System")

    # Creating sliders for each category
    comedy_rating = st.slider("Comedy", 1, 10, 5)
    romance_rating = st.slider("Romance", 1, 10, 5)
    drama_rating = st.slider("Drama", 1, 10, 5)
    action_rating = st.slider("Action", 1, 10, 5)
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
                'Drama': drama_rating,
                'Action': action_rating,
                'Acting Performance': acting_performance_rating,
                'Engagingness': engagingness_rating
            },
            'num_movies': 5  # Or however many movies you want to get back from the backend
        }

        # Get movie recommendations
        response = get_movie_recommendations(data)
        print("Data received from Flask:", response.json())

    # Display results if response is available
    if response:
        if response.status_code == 200:
            results = response.json()
            st.write("Movie Recommendations:")

            # Number of movies to display
            num_movies = len(results)

            # Create columns for each movie
            cols = st.columns(num_movies)

            for i, movie in enumerate(results):
                with cols[i]:
                    # Display the image of each movie
                    if movie["Image URL"]:
                        st.image(movie["Image URL"], use_column_width=True)
                    else:
                        st.write("No image available")
        else:
            st.error(f"Failed to get response from Flask. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
