import requests

url = "https://api.themoviedb.org/3/search/movie"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYTA2ZTY3MzM2ZTg0M2FhZjE3NTQ0NTIyOGI4MzgzOSIsIm5iZiI6MTc3OTM5MTE3NC4zNzIsInN1YiI6IjZhMGY1YWM2ZjYyY2MwNDYwZDNkZWUwMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FvRvl9AxiznUHTog4JvdPPVjbgUrHyAr65iecv3cVQM"
}
"""
function for search film and added in a list, 
for show the user when her searched
"""
def get_films(film) -> dict:

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

