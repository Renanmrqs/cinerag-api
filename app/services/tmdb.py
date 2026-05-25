from fastapi import Depends
from app.models import Movies
import requests
from app.models import Movies
from sqlalchemy.orm import Session
from app.database import get_db



"""
function for search film and added in a list, 
for show the user when her searched
"""
def get_films(film) -> dict:
    url = "https://api.themoviedb.org/3/search/movie"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYTA2ZTY3MzM2ZTg0M2FhZjE3NTQ0NTIyOGI4MzgzOSIsIm5iZiI6MTc3OTM5MTE3NC4zNzIsInN1YiI6IjZhMGY1YWM2ZjYyY2MwNDYwZDNkZWUwMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FvRvl9AxiznUHTog4JvdPPVjbgUrHyAr65iecv3cVQM"
    }
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
function for get the median for reviews of one movie.
using for generate this, return general of review and save on database
"""
def get_score(list_review) -> int:
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
    media = sentiment_score_dict['trust'] / total_reviews
    sentiment_score_dict['trust'] = media    

    return sentiment_score_dict

print(get_score(["horrible. i hated", 'miserable filme, ridiculos i hated', 'great film dude, i loved it', 'awlful film, horrible again, i dont like her', 'great, i liked it', 'amazinggg filme, greates all time']))

"""
function for search a film with id, one film something
"""
def get_film_id(id, db) -> dict:
    film = db.query(Movies).filter(Movies.id == id).first()
    if film:
        return film.sentiment_trust, film.sentiment    
    else:
        
        url = "https://api.themoviedb.org/3/movie/{movie_id}/reviews"
        headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYTA2ZTY3MzM2ZTg0M2FhZjE3NTQ0NTIyOGI4MzgzOSIsIm5iZiI6MTc3OTM5MTE3NC4zNzIsInN1YiI6IjZhMGY1YWM2ZjYyY2MwNDYwZDNkZWUwMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FvRvl9AxiznUHTog4JvdPPVjbgUrHyAr65iecv3cVQM"
        }
        response = requests.get(url, headers=headers, params={"query": f"{id}"})
        data = response.json()
        reviews = []
        for result in data["results"]:
            if result["content"] not in reviews:
                reviews.append(result["content"])    
        """
        pega o reviw, retornar so o review, dps usar GET /movie/{id}
        pra pegar as infors do filme que o sentimento foi gerado, pega o sentimento todo
        e salva no banco de dados, para dpois n precisar usar toda hora a api do tmdb
        """
        review_score = get_score(reviews)
        if review_score['positive'] > review_score['negative']:
            return 'positive', review_score['trust']
        elif review_score['negative'] > review_score['positive']:
            return 'negative', review_score['trust']
        else:
            return 'mixed', review_score['trust']
        

    """
    fazeer o salvamento no banco de dados para pertinencia
    """


            
# url = "https://api.themoviedb.org/3/movie/550/reviews"
# headers = {
# "accept": "application/json",
# "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYTA2ZTY3MzM2ZTg0M2FhZjE3NTQ0NTIyOGI4MzgzOSIsIm5iZiI6MTc3OTM5MTE3NC4zNzIsInN1YiI6IjZhMGY1YWM2ZjYyY2MwNDYwZDNkZWUwMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FvRvl9AxiznUHTog4JvdPPVjbgUrHyAr65iecv3cVQM"
# }
# response = requests.get(url, headers=headers)
# data = response.json()
# print(data)
# for result in data["results"]:
#     reviews = []
#     if result["content"] not in reviews:
#         reviews.append(result["content"])    
# print(reviews)