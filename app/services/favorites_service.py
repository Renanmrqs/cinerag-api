from app.models import Favorites, Movies, UserPreferences, Genres
from sqlalchemy.orm import Session
from sqlalchemy import delete
from datetime import date
from app.clients.tmdb_client import client_get_detail_movie
from app.services.user_preferences_service import add_user_preferences, del_user_preferences

"""
post on table favorites
"""  
def create_favorite(user_id, movie_id, db: Session) -> dict:
    favorite = Favorites(user_id=user_id, movie_id=movie_id, added_at=date.today())
    db.add(favorite)
    detail_movie = client_get_detail_movie(movie_id)
    
    for detail in detail_movie.get('genres', []):
        add_user_preferences(detail['id'], user_id, db)
    
    db.commit()
    db.refresh(favorite)
    return {'message': 'film added!'}




"""
read all favorites on db
"""
def read_all_favorites(user_id, db:Session) -> dict:
    favorite_table = db.query(Favorites.id, Favorites.added_at, Movies.title, Movies.sentiment, Movies.sentiment_trust).filter(Favorites.user_id == user_id).join(Movies, Favorites.movie_id == Movies.id).all()
    return [{"id": r.id, "title": r.title, "added_at": r.added_at, "sentiment": r.sentiment, "trust": r.sentiment_trust} for r in favorite_table]


"""
read all films on table favorites
"""
def readl_all_films(user_id, db:Session) -> dict:
    favorite_table = db.query(Favorites.id, Favorites.added_at, Movies.title, Movies.sentiment, Movies.sentiment_trust).filter(Favorites.user_id == user_id).join(Movies, Favorites.movie_id == Movies.id).all()
    return [{"title": r.title} for r in favorite_table]

"""
delete a fav
"""
def delete_fav(id, db:Session) -> dict:
    fav = db.query(Favorites).filter(Favorites.id == id).first()
    if not fav:
        return None
    detail_movie = client_get_detail_movie(fav.movie_id)
    for detail in detail_movie.get('genres', []):
        del_user_preferences(detail['id'], fav.user_id, db)
    
    db.delete(fav)
    db.commit()
    return {'message': 'film deleted'}