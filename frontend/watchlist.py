import streamlit as st
import requests

def show_watch_list():
    # Define the URL of the Flask API endpoint
    url = "http://127.0.0.1:5000/test_db_connection"
    
    # Perform a GET request to the Flask API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # If successful, get JSON data from the response
        data = response.json()
        
        # Display the data in Streamlit
        st.write("Database Connection Status:", data["message"])
        
        # Check if the "data" key is in the response and display it
        if "data" in data:
            st.write("Data from the database:", data["data"])
    else:
        # If the request was not successful, display an error message
        st.write("Failed to retrieve data from the backend. Status code:", response.status_code)


