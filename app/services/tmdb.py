from app.models import Movies
import requests
from sqlalchemy.orm import Session
from datetime import date

headers = {
"accept": "application/json",
"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYTA2ZTY3MzM2ZTg0M2FhZjE3NTQ0NTIyOGI4MzgzOSIsIm5iZiI6MTc3OTM5MTE3NC4zNzIsInN1YiI6IjZhMGY1YWM2ZjYyY2MwNDYwZDNkZWUwMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FvRvl9AxiznUHTog4JvdPPVjbgUrHyAr65iecv3cVQM"
}


"""
function for search film and added in a list, 
for show the user when her searched
"""
def get_films(film) -> dict:
    url = "https://api.themoviedb.org/3/search/movie"
    films_listed = []
    response = requests.get(url, headers=headers, params={"query": f"{film}"})
    data = response.json()
    for result in data['results']:
        films = {'id': '', 'title': '', 'language': '', 'overview': '', 'release_date': ''}
        if result['id'] not in [films_listed]:  
            films.update({'id': result['id'], 
            'title': result['title'],
            'language': result['original_language'],
            'overview': result['overview'],
            'release_date': result['release_date']
            })
            films_listed.append(films)
    return films_listed


"""
auxiliar function: to search my own predict model, using the reviews from tmdb
"""
def get_movie_sentiment(list_review: list) -> dict:
    url = "https://sentimentai-api.onrender.com/predict"
    sentiment_score_dict = {'positive': 0, 'negative': 0,
    'trust': 0}
    total_reviews = len(list_review)
    
    for review in list_review:
        response = requests.post(url, json={"text": review})
        data = response.json()
        match data['sentiment']:
            case 'positive':
                sentiment_score_dict['positive'] += 1
            case 'negative':
                sentiment_score_dict['negative'] += 1
        sentiment_score_dict['trust'] += data['trust']
    if total_reviews <= 0:
        return sentiment_score_dict
    media = sentiment_score_dict['trust'] / total_reviews
    sentiment_score_dict['trust'] = media    
    return sentiment_score_dict


"""
auxiliar function: using for saving the data of movies if not in db
"""
def get_detail_movie(id: int) -> dict:
    url = f"https://api.themoviedb.org/3/movie/{id}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


"""
auxiliar function: using for searchin each reviews for a movie id
"""
def get_reviews_from_movies(id: int) -> dict:
    url = f"https://api.themoviedb.org/3/movie/{id}/reviews"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


"""
function for search a film with id, return score(positive or negative or mixed and trusted)
and save this on db for pertinence
"""
def get_film_score(id ,db: Session) -> dict:
    data = get_reviews_from_movies(id)
    reviews = []
    for result in data["results"]:
        reviews.append(result["content"])  
    
    movie = db.query(Movies).filter(Movies.id == id).first()
    if movie:
        return {'sentiment': movie.sentiment, 'trust': movie.sentiment_trust, 'title': movie.title, 'sample_reviews': reviews[:3]}
  


    # using the movie sentiment and detail for saving on db

    movie_sentiment = get_movie_sentiment(reviews[:10]) 
    detail_movie = get_detail_movie(id)
    
    if movie_sentiment['positive'] > movie_sentiment['negative']:
        sentiment = 'positive'
    elif movie_sentiment['negative'] > movie_sentiment['positive']:
        sentiment = 'negative'
    else:
        sentiment = 'mixed'

    movie = Movies(id=detail_movie['id'], title=detail_movie['title'], sentiment_trust=movie_sentiment['trust'], sentiment=sentiment, analyzed_at=date.today())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return {'sentiment': sentiment, 'trust': movie_sentiment['trust'], 'title': detail_movie['title'], 'sample_reviews': reviews[:3]}

    """_summary_
    retornar ao menos 3 reviews por filme sacou
    """
        


