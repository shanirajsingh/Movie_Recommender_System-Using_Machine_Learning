import streamlit as st
import pickle
import pandas as pd
import requests
import time
"""
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=eb4d77723f12afc5953bd5442187fa0b&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
"""
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=eb4d77723f12afc5953bd5442187fa0b&language=en-US"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise error for bad status codes
        
        data = response.json()
        
        poster_path = data.get('poster_path')
        
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            # If poster not available
            return "https://via.placeholder.com/500x750?text=No+Image"
    
    except requests.exceptions.ConnectionError:
        print("Connection Error: Network or DNS issue")
        return "https://via.placeholder.com/500x750?text=Connection+Error"
    
    except requests.exceptions.Timeout:
        print("Timeout Error: Server took too long to respond")
        return "https://via.placeholder.com/500x750?text=Timeout"
    
    except requests.exceptions.RequestException as e:
        print("API Error:", e)
        return "https://via.placeholder.com/500x750?text=API+Error"

"""def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
   
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  

        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch poster from api
        import time
        for i in movies_list:
            recommended_movies_posters.append(fetch_poster(movie_id))
            time.sleep(0.3)  # small delay
        # recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters
"""

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

        #time.sleep(0.3)   # small delay to avoid rate limit

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity =  pickle.load(open('similarity.pkl','rb'))

st.title(' Movie Recommender System')

selected_movie_name = st.selectbox(
"How would you like to be contacted?",
movies['title'].values
)

if st.button("Recommend", type="primary"):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

