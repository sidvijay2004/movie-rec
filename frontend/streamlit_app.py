import streamlit as st
import requests

# Define a function to send ratings to the Flask backend and get the results
@st.cache_data(show_spinner=True)
def get_movie_recommendations(data):
    # Sending data to Flask and getting response
    print("Data sent to backend:", data)
    response = requests.post('http://localhost:5000/process_ratings', json=data)
    return response

def main():
    st.title("Movie Rating System")

    # Creating sliders for each category
    comedy_rating = st.slider("Comedy", 1, 10, 5)
    romance_rating = st.slider("Romance", 1, 10, 5)
    action_rating = st.slider("Action", 1, 10, 5)
    drama_rating = st.slider("Drama", 1, 10, 5)
    acting_performance_rating = st.slider("Acting Performance", 1, 10, 5)
    engagingness_rating = st.slider("Engagingness", 1, 10, 5)

    # Submit button
    if st.button('Submit Ratings'):
        # Prepare data to be sent to Flask
        data = {
            'ratings': {
                'comedy': comedy_rating,
                'romance': romance_rating,
                'action': action_rating,
                'drama': drama_rating,
                'acting_performance': acting_performance_rating,
                'engagingness': engagingness_rating
            },
            'num_movies': 5  # Or however many movies you want to get back from the backend
        }

        # Invalidate the cache when the button is pressed
        st.cache_data.clear()

        # Get movie recommendations
        response = get_movie_recommendations(data)

        # Check the response status and display the results
        if response.status_code == 200:
            results = response.json()
            st.write("Response from Flask:")
            st.json(results)
        else:
            st.error(f"Failed to get response from Flask. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
