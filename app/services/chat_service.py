from app.services.querys_service import positive_movie, smaller_trusted, most_trusted, negative_movie, mixed_movie, count_films, first_added, last_added
from app.clients.gemini_client import gemini_func
from app.core.logging import logger

def service_query(data, username, db):
    try:
        if data == '/positives':
            result = positive_movie(username, db)
            return result
        elif data == '/negatives':
            result = negative_movie(username, db)
            return result
        elif data == '/mixeds':
            result = mixed_movie(username, db)
            return result
        elif data == '/most trusted':
            result = most_trusted(username, db)
            return result
        elif data == '/count films':
            result = count_films(username, db)
            return result
        elif data == '/smaller trusted':
            result = smaller_trusted(username, db)
            return result
        elif data == '/first film added':
            result = first_added(username, db)
            return result
        elif data == '/last film added':
            result = last_added(username, db)
            return result
        else:
            result = gemini_func(username, data, db)
            return result
    except Exception as e:
        logger.error(f"Service Query error - user: {username} | error: {str(e)}")
        raise

    
    