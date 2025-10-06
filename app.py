import os
import requests
import pickle

def download_file(url, destination):
    if not os.path.exists(destination):
        print(f"Downloading {destination} ...")
        response = requests.get(url)
        with open(destination, "wb") as f:
            f.write(response.content)
    else:
        print(f"{destination} already exists, skipping download.")

os.makedirs("artificats", exist_ok=True)

movie_list_url = "https://dl.dropboxusercontent.com/scl/fi/jzow4g8h5k8wc70kcap2o/movie_list.pkl"
similarity_url = "https://dl.dropboxusercontent.com/scl/fi/wgu40u5v6xpcu29sq6y8z/similarity.pkl"

download_file(movie_list_url, "artificats/movie_list.pkl")
download_file(similarity_url, "artificats/similarity.pkl")

movies = pickle.load(open("artificats/movie_list.pkl", "rb"))
similarity = pickle.load(open("artificats/similarity.pkl", "rb"))


import pickle
import streamlit as st
import requests


import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=29b0ac573607db6951a0561000487bb0&language=en-US"
        response = requests.get(url, timeout=10)

        # If API request fails
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            return "https://via.placeholder.com/500x750?text=No+Poster"

        data = response.json()

        # Some movies may not have poster_path
        poster_path = data.get("poster_path")
        if not poster_path:
            return "https://via.placeholder.com/500x750?text=No+Poster"

        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        # Return placeholder image instead of crashing
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movies_name = []
    recommended_movies_poster = []
    
    for i in distances[1:6]:  # top 5 similar movies
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_name.append(movies.iloc[i[0]].title)   # <-- FIXED (add names)
        recommended_movies_poster.append(fetch_poster(movie_id))  # posters
    
    return recommended_movies_name, recommended_movies_poster


st.header("Movies Reccomendation System Using Machine Learning")
movies = pickle.load(open('artificats/movie_list.pkl','rb'))
similarity = pickle.load(open('artificats/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get recommendation',
    movie_list
) 

if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
         st.text(recommended_movies_name[0])
         st.image(recommended_movies_poster[0])
    with col2:
         st.text(recommended_movies_name[1])
         st.image(recommended_movies_poster[1])
    with col3:
         st.text(recommended_movies_name[2])
         st.image(recommended_movies_poster[2])
    with col4:
         st.text(recommended_movies_name[3])
         st.image(recommended_movies_poster[3])
    with col5:
         st.text(recommended_movies_name[4])
         st.image(recommended_movies_poster[4])



