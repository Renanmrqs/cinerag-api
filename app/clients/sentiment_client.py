import requests
from app.core.logging import logger

"""
function for search movie_sentiments
"""
def client_movie_sentiment(review):
    url = "https://sentimentai-api.onrender.com/predict"
    try:
        response = requests.post(url, json={"text": review})
        data = response.json()
        return data
    except Exception as e:
        logger.error(f"sentiment API error: {e}")
        raise