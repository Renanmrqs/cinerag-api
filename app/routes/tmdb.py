# import requests
# from dotenv import load_dotenv
# import os

# load_dotenv()
# BASE_URL = os.getenv('TMD_KEY')

# response = requests.get(f'{BASE_URL}')

import requests

url = "https://api.themoviedb.org/3/search/movie"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYTA2ZTY3MzM2ZTg0M2FhZjE3NTQ0NTIyOGI4MzgzOSIsIm5iZiI6MTc3OTM5MTE3NC4zNzIsInN1YiI6IjZhMGY1YWM2ZjYyY2MwNDYwZDNkZWUwMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FvRvl9AxiznUHTog4JvdPPVjbgUrHyAr65iecv3cVQM"
}

response = requests.get(url, headers=headers, params={"query": "Fight Club", "language": "en-US"})

print([page for page in response.json()['results']])