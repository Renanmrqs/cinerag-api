from app.models import Movies
from app.clients.tmdb_client import client_get_films, client_get_reviews_from_movies, client_get_detail_movie
from app.clients.sentiment_client import client_movie_sentiment
from sqlalchemy.orm import Session
from datetime import date



"""
function for search film and added in a list, 
for show the user when her searched
"""

def get_films(film) -> list:
    data = client_get_films(film)
    films_listed = []
    
    for result in data['results']:
        reviews = client_get_reviews_from_movies(result['id'])

        films = {'id': '', 'title': '', 'language': '', 'overview': '', 'release_date': ''}
        if not any(f['id'] == result['id'] for f in films_listed):  
            films.update({'id': result['id'], 
            'title': result['title'],
            'language': result['original_language'],
            'overview': result['overview'],
            'release_date': result['release_date'],
            'has_reviews': True
            })
            if len(reviews['results']) < 1:
                films.update({'has_reviews': False})
            films_listed.append(films)
    return films_listed


"""
auxiliar function: to search my own predict model, using the reviews from tmdb
"""
def get_movie_sentiment(list_review: list) -> dict:
    sentiment_score_dict = {'positive': 0, 'negative': 0,
    'trust': 0}
    total_reviews = len(list_review)
    
    for review in list_review:
        
        data = client_movie_sentiment(review)
        
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
function for search a film with id, return score(positive or negative or mixed and trusted)
and save this on db for pertinence
"""
def get_film_score(id ,db: Session) -> dict:
    data = client_get_reviews_from_movies(id)
    reviews = []
    for result in data["results"]:
        reviews.append(result["content"])  
    
    movie = db.query(Movies).filter(Movies.id == id).first()
    if movie:
        return {'sentiment': movie.sentiment, 'trust': movie.sentiment_trust, 'title': movie.title, 'sample_reviews': reviews[:3]}
  

    # using the movie sentiment and detail for saving on db

    movie_sentiment = get_movie_sentiment(reviews[:30]) 
    detail_movie = client_get_detail_movie(id)
    
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




    

