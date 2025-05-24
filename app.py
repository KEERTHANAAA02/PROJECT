import streamlit as st
from recommendation import (
    get_all_movie_titles,
    get_content_recommendations,
    get_collaborative_recommendations,
    get_all_genres,
    get_movies_by_genre
)

st.set_page_config(page_title="Movie Recommender", layout="centered")

st.title("🎬 Movie Recommendation System")

# Sidebar navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose a recommendation method:", 
                          ["Genre Based", "Content Based", "Collaborative Filtering"])

st.markdown("## 🔍 Get Movie Suggestions")

if option == "Genre Based":
    st.subheader("🎭 Genre-Based Recommendation")
    genres = get_all_genres()
    genre_selected = st.selectbox("Select a genre:", genres)
    
    if st.button("Show Movies"):
        movies = get_movies_by_genre(genre_selected)
        if movies:
            st.success(f"Top movies in **{genre_selected.title()}** genre:")
            for m in movies[:10]:
                st.write(f"- {m}")
        else:
            st.warning("No movies found for this genre.")

elif option == "Content Based":
    st.subheader("📽️ Content-Based Recommendation")
    titles = get_all_movie_titles()
    selected_title = st.selectbox("Choose a movie you like:", titles)
    
    if st.button("Recommend Similar Movies"):
        recommendations = get_content_recommendations(selected_title)
        if recommendations and "not found" not in recommendations[0].lower():
            st.success("You may also like:")
            for movie in recommendations:
                st.write(f"- {movie}")
        else:
            st.warning("No similar movies found.")

elif option == "Collaborative Filtering":
    st.subheader("👥 Collaborative Filtering Recommendation")
    titles = get_all_movie_titles()
    selected_title = st.selectbox("Choose a movie you've rated or liked:", titles)
    
    if st.button("Find Collaborative Recommendations"):
        recommendations = get_collaborative_recommendations(selected_title)
        if recommendations and "not rated" not in recommendations[0].lower():
            st.success("Users who liked this also liked:")
            for movie in recommendations:
                st.write(f"- {movie}")
        else:
            st.warning("Not enough data for this movie.")
