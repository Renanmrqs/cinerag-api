import os
from dotenv import load_dotenv
import requests
from app.core.logging import logger

load_dotenv()

headers = {
"accept": "application/json",
"Authorization": f"Bearer {os.getenv('TMDB_TOKEN')}"
}

"""
service for searching movies
"""
def client_get_films(film) -> dict:
    url = "https://api.themoviedb.org/3/search/movie"
    try:
        response = requests.get(url, headers=headers, params={"query": f"{film}"})
        data = response.json()
        return data
    except Exception as e:
        logger.error(f"TMDB API error: {e}")
        raise

"""
auxiliar service: using for searchin each reviews for a movie id
"""
def client_get_reviews_from_movies(id: int) -> dict:
    url = f"https://api.themoviedb.org/3/movie/{id}/reviews"
    try:    
        response = requests.get(url, headers=headers)
        data = response.json()
        return data
    except Exception as e:
        logger.error(f"TMDB API error: {e}")
        raise


"""
auxiliar function: using for saving the data of movies if not in db
"""
def client_get_detail_movie(id: int) -> dict:
    url = f"https://api.themoviedb.org/3/movie/{id}"
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data
    except Exception as e:
        logger.error(f"TMDB API error: {e}")
        raise