import streamlit as st
import requests

# Use Streamlit's caching to prevent re-fetching the same data on each rerun
# @st.cache_data
def get_watch_list():
    url = "http://127.0.0.1:5000/test_db_connection"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"message": f"Failed to retrieve data. Status code: {response.status_code}", "data": []}

def show_watch_list():
    data = get_watch_list()
    
    st.write("Database Connection Status:", data["message"])
    
    if "data" in data and data["data"]:
        for entry in data["data"]:
            # Use the 'image_url' key from each entry to display the image
            if entry.get("image_url"):  # Make sure there is a URL
                st.image(entry["image_url"], width=300)
            else:
                st.write("No image available for:", entry["title"])
    else:
        st.write("No data available.")


