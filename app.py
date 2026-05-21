import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gzip
import numpy as np

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ---------------- FETCH POSTER ---------------- #

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):

    try:
        api_key = st.secrets["TMDB_API_KEY"]

    except:
        st.error("TMDB API Key not found in Streamlit Secrets")
        return "https://via.placeholder.com/500x750?text=API+Key+Missing"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

        return "https://via.placeholder.com/500x750?text=No+Poster"

    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=Error"


# ---------------- LOAD FILES ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies_path = os.path.join(BASE_DIR, "movie_dict.pkl")
similarity_path = os.path.join(BASE_DIR, "similarity.pkl.gz")

# load movies
with open(movies_path, "rb") as f:
    movies_dict = pickle.load(f)

movies = pd.DataFrame(movies_dict)

# load compressed similarity
with gzip.open(similarity_path, "rb") as f:
    similarity = pickle.load(f)

# ---------------- RECOMMEND FUNCTION ---------------- #

def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    # top 5 similar movies
    movies_list = np.argsort(distances)[::-1][1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:

        movie_id = movies.iloc[i].movie_id

        recommended_movies.append(
            movies.iloc[i].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_posters


# ---------------- UI ---------------- #

st.title("🎬 Movie Recommender System")

st.markdown("Get movie recommendations instantly")

selected_movie_name = st.selectbox(
    "Choose a movie",
    movies['title'].values
)

if st.button("Recommend"):

    with st.spinner("Fetching recommendations..."):

        names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for idx, col in enumerate(cols):

        with col:
            st.text(names[idx])
            st.image(posters[idx])


# ---------------- FOOTER ---------------- #

st.markdown("---")
st.caption("Built with Streamlit ❤️")

