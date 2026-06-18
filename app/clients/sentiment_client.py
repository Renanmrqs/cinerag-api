import requests

"""
function for search movie_sentiments
"""
def client_movie_sentiment(review):
    url = "https://sentimentai-api.onrender.com/predict"
    response = requests.post(url, json={"text": review})
    data = response.json()
    return data