
import streamlit as st
import joblib
from io import BytesIO
import requests
import imdb
from PIL import Image
import numpy as np
import pandas as pd
from streamlit.components.v1 import html

similarityData = joblib.load("similarity.pkl")

movieSet = pd.read_csv("filteredSet.csv")

totalMovieToReturn = 5
searchHistory = []

# Reccomending movie based on Genre and Ratings
def returnReccomendation(movieTitle,total,df = movieSet,similarityData=similarityData):
    index = np.where(df.Title==movieTitle)[0][0]
    similarity = similarityData[index]
    sortedData =list(enumerate(similarity))
    sortedData.sort(key=lambda x:x[1],reverse=True)
    top = [value[0] for value in sortedData[:total]]
    reccomendedDf = movieSet.iloc[top,:]
    finalDf = reccomendedDf.sort_values("Rating")[::-1]
    titles = finalDf.loc[:,["Title"]]
    return titles # returns the title and index (DataFrame)

# Searcing image link in imdb
def returnImage(title):
    movieDB = imdb.IMDb()
    results = movieDB.search_movie(title)[0]
    link= results.values()[-1]
    img = requests.get(link).content
    img = BytesIO(img)
    image = Image.open(img).resize((220,320))
    return image

def MovieDetail(title):
    movieDB = imdb.IMDb()
    results = movieDB.search_movie(title)[0]
    link = movieDB.get_imdbURL(results)

    details = movieSet[movieSet.Title==title]
    name = list(details.Title)[0]
    rating = list(details.Rating)[0]
    director = list(details.Director)[0]
    runTime = list(details["Duration (min)"])[0]
    cast = list(details.Cast)[0]
    description = list(details.Description)[0]
    certificate = list(details.Certificate)[0]
    year = list(details.Year)[0]
    genre = list(details.Genre)[0]
    image = returnImage(title)
    
    #### Streamlit host
    

    selectedMovieContainer = st.container(height=350,border=True)
    imageCol, bodyCol = selectedMovieContainer.columns([1,2])
    imageCol.image(image=image)
    bodyCol.subheader(f"[{name} ({certificate})]({link})")
    bodyCol.write(f"Genre: {genre}  (IMDb: {rating})")
    # bodyCol.write(f"Duration: {int(runTime)} Minutes ")
    bodyCol.write(f"Director: {director}")
    bodyCol.write(f"Cast and Crew: {cast}")
    bodyCol.write(f"Description: {description}")


def plotRecMovies(movies): 
    for value in range(len(movies)):
        MovieDetail(movies[value])


st.title("Movie Recommendation System")
movie_selected = st.selectbox(options = movieSet.Title,label="Select You Favourite Movie")
if st.button("Search"):
    # ploting selected movie
    
    st.subheader("Your Favourite Movie")
    MovieDetail(movie_selected)
    st.subheader("Recommended Movies")
    reccomendadeMovieTitle = returnReccomendation(movieTitle=movie_selected,total=totalMovieToReturn+1)
    all_titles = list(reccomendadeMovieTitle.Title)
    if movie_selected in all_titles:
        all_titles.remove(movie_selected)
    else:
        all_titles.pop()
    
    plotRecMovies(all_titles)
    st.warning("This Recommendation is based on Genre and Ratings on IMDb page.")
    # ploting reccomendade movies
   