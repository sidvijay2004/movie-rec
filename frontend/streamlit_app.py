import streamlit as st
import requests

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
            'comedy': comedy_rating,
            'romance': romance_rating,
            'action': action_rating,
            'drama': drama_rating,
            'acting_performance': acting_performance_rating,
            'engagingness': engagingness_rating
        }
        # Sending data to Flask and getting response
        response = requests.post('http://localhost:5000/process_ratings', json=data)
        if response.status_code == 200:
            results = response.json()
            st.write("Response from Flask:")
            st.json(results)
        else:
            st.write("Failed to get response from Flask")

if __name__ == "__main__":
    main()
