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

def generate_dummy_user_ratings(movies):
    """Generate dummy user ratings for demonstration purposes."""
    user_ratings = {
        "userId": [1, 1, 1, 2, 2, 2],
        "movieId": [movies.iloc[0]["movieId"], movies.iloc[1]["movieId"], movies.iloc[2]["movieId"],
                    movies.iloc[3]["movieId"], movies.iloc[4]["movieId"], movies.iloc[5]["movieId"]],
        "rating": [5, 4, 3, 5, 4, 2]
    }
    return pd.DataFrame(user_ratings)

def train_recommendation_model(user_ratings):
    """Train a collaborative filtering recommendation model."""
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(user_ratings[['userId', 'movieId', 'rating']], reader)
    trainset, testset = train_test_split(data, test_size=0.2)

    model = SVD()  # Singular Value Decomposition model
    model.fit(trainset)
    
    predictions = model.test(testset)
    accuracy.rmse(predictions)
    
    return model

def recommend_movies(model, user_id, movies, top_n=5):
    """Recommend movies for a given user."""
    movie_ids = movies["movieId"].tolist()
    rated_movie_ids = user_ratings[user_ratings["userId"] == user_id]["movieId"].tolist()
    unrated_movie_ids = [mid for mid in movie_ids if mid not in rated_movie_ids]

    recommendations = []
    for movie_id in unrated_movie_ids:
        pred = model.predict(user_id, movie_id)
        recommendations.append((movie_id, pred.est))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)
    recommended_movies = [movies[movies["movieId"] == rec[0]]["title"].values[0] for rec in recommendations[:top_n]]
    return recommended_movies

if __name__ == "__main__":
    # Fetch data from TMDb
    movies = fetch_movie_data()
    print("Movies Data:")
    print(movies.head())

    # Generate dummy user ratings
    user_ratings = generate_dummy_user_ratings(movies)
    print("\nUser Ratings:")
    print(user_ratings)

    # Train collaborative filtering model
    model = train_recommendation_model(user_ratings)

    # Recommend movies for a user
    user_id = 1
    recommendations = recommend_movies(model, user_id, movies, top_n=5)
    print(f"\nRecommended Movies for User {user_id}:")
    for movie in recommendations:
        print(movie)
