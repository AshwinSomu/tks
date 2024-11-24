import requests
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

# TMDb API key (Replace with your own)
API_KEY = "your_tmdb_api_key"

def fetch_movie_data():
    """Fetch popular movies from TMDb."""
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    data = response.json()
    movies = data['results']
    
    # Extract relevant movie information
    movie_data = []
    for movie in movies:
        movie_data.append({
            "movieId": movie["id"],
            "title": movie["title"],
            "rating": round(movie["vote_average"], 1)
        })
    return pd.DataFrame(movie_data)

# Remaining code follows...
