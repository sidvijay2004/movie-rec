import streamlit as st
from movie_recommendations import show_movie_recommendations
from watchlist import show_watch_list
# from another_feature import show_another_feature
# Import other pages as needed

def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.selectbox("Choose a function", 
                                  ["Movie Recommendations", "Watchlist"])

    if choice == "Movie Recommendations":
        show_movie_recommendations()
    elif choice == "Watchlist":
        show_watch_list()

if __name__ == "__main__":
    main()
