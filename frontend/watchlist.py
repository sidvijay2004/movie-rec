import streamlit as st
import requests

# Use Streamlit's caching to prevent re-fetching the same data on each rerun
# @st.cache(allow_output_mutation=True)
def get_watch_list():
    url = "http://127.0.0.1:5000/test_db_connection"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"message": f"Failed to retrieve data. Status code: {response.status_code}", "data": []}

def update_watch_status(updates):
    url = "http://127.0.0.1:5000/update_watch_status"
    response = requests.put(url, json=updates)
    if response.status_code == 200:
        st.success("Watch statuses updated successfully!")
    else:
        st.error(f"Failed to update watch statuses. Error: {response.text}")


def show_watch_list():
    data = get_watch_list()
    st.write("Database Connection Status:", data["message"])

    if "data" in data and data["data"]:
        # Initialize session state for delete tracking if not already set
        if 'delete_ids' not in st.session_state:
            st.session_state.delete_ids = []

        with st.form(key='watch_list_form'):
            updates = []

            for idx, entry in enumerate(data["data"]):
                col1, spacer, col2, col3, col4, delete_col = st.columns([1, 0.2, 1.5, 1.3, 2.5, 0.5])
                with col1:
                    if entry.get("image_url"):
                        st.image(entry["image_url"], width=100)
                with col2:
                    st.write(entry["title"])
                with col3:
                    watched = st.checkbox("Watched", key=f"watched_{entry['id']}", value=bool(entry["watched"]))
                    updates.append({"id": entry["id"], "watched": watched})
                with col4:
                    similar_movies = fetch_similar_movies_from_backend(entry['tmdb_id'])
                    if similar_movies:
                        with st.expander(f"Similar Movies for {entry['title']}"):
                            for movie in similar_movies:
                                formatted_movie_info = f"{movie['title']} - {movie['vote_average']}/10"
                                st.write(formatted_movie_info)
                    else:
                        st.write("No similar movies found")
                with delete_col:
                    # Use checkboxes for deletion to avoid instant removal and allow batch operations
                    delete_action = st.checkbox("🗑️", key=f"delete_{entry['id']}")
                    if delete_action:
                        # Add to session state list if checked
                        st.session_state.delete_ids.append(entry["id"])
                    elif entry["id"] in st.session_state.delete_ids:
                        # Remove from session state list if unchecked
                        st.session_state.delete_ids.remove(entry["id"])
            
            submitted = st.form_submit_button("Submit Changes")

        # Handle the submission outside of the form
        if submitted:
            if updates:
                update_watch_status(updates)
            if st.session_state.delete_ids:
                remove_from_watchlist(st.session_state.delete_ids)
                # Clear the session state after deletion
                st.session_state.delete_ids = []
                st.experimental_rerun()  # Rerun the app to reflect the deletions
    else:
        st.write("No data available.")


def fetch_similar_movies_from_backend(tmdb_id):
    url = f"http://127.0.0.1:5000/get_similar_movies/{tmdb_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch similar movies.")
        return []

def remove_from_watchlist(movie_ids):
    # This function now expects a list of movie IDs to remove
    url = f"http://127.0.0.1:5000/remove_from_watchlist"
    response = requests.delete(url, json={"movie_ids": movie_ids})
    return response.status_code == 200
