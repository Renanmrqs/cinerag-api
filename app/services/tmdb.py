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
def get_score(list_review) -> list:
    pass

"""
function for search a film with id, one film something
"""
def get_film_id(id, db) -> dict:
    film = db.query(Movies).filter(Movies.id == id).first()

    if film:
        return film.sentiment_score
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
        pegar o reviw, retornar so o review, dps usar GET /movie/{id}
        pra pegar as infors do filme que o sentimento foi gerado, pegar o sentimento todo
        e salvar no banco de dados, para dpois n precisar usar toda hora a api do tmdb
        """
        # review_score = get_score(reviews)




            
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