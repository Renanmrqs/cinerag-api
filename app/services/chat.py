from app.models import Favorites, Movies, ChatHistory
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date
from app.services.auth import get_user_id

# def read_all_favorites(user_id, db:Session) -> dict:
#     favorite_table = db.query(Favorites.id, Favorites.added_at, Movies.title, Movies.sentiment, Movies.sentiment_trust).filter(Favorites.user_id == user_id).join(Movies, Favorites.movie_id == Movies.id).all()
#     return [{"id": r.id, "title": r.title, "added_at": r.added_at, "sentiment": r.sentiment, "trust": r.sentiment_trust} for r in favorite_table]
    

# def create_favorite(user_id, movie_id, db:Session) -> dict:
#     favorite = Favorites(user_id=user_id, movie_id=movie_id, added_at=date.today())
#     db.add(favorite)
#     db.commit()
#     db.refresh(favorite)
#     return {'message': 'film added!'}
"""
search all positive films
"""
def positive_movie (username, db):
    user_id = get_user_id(username, db)
    positive = db.query(Favorites.id, Favorites.added_at, Movies.title, Movies.sentiment, Movies.sentiment_trust).filter(Favorites.user_id == user_id, Movies.sentiment == 'positive').join(Movies, Favorites.movie_id == Movies.id).all()
    if not positive:
        return "nothing in the favorites list"
    return f"Positive films: {', '.join([c.title for c in positive])}"
"""
search all negative movies
"""
def negative_movie (username, db):
    user_id = get_user_id(username, db)
    negative = db.query(Favorites.id, Favorites.added_at, Movies.title, Movies.sentiment, Movies.sentiment_trust).filter(Favorites.user_id == user_id, Movies.sentiment == 'negative').join(Movies, Favorites.movie_id == Movies.id).all()
    if not negative:
        return "nothing in the favorites list"
    return f"Negative films: {', '.join([c.title for c in negative])}"

"""
search all mixed movies
"""
def mixed_movie (username, db):
    user_id = get_user_id(username, db)
    mixed = db.query(Favorites.id, Favorites.added_at, Movies.title, Movies.sentiment, Movies.sentiment_trust).filter(Favorites.user_id == user_id, Movies.sentiment == 'mixed').join(Movies, Favorites.movie_id == Movies.id).all()
    if not mixed:
        return "nothing in the favorites list"
    return f"Mixed films: {', '.join([c.title for c in mixed])}"

"""
search most trusted film
"""
def most_trusted (username, db):
    user_id = get_user_id(username, db)
    trusted = db.query(Favorites.id, Favorites.added_at, Movies.title, Movies.sentiment, Movies.sentiment_trust).filter(Favorites.user_id == user_id).join(Movies, Favorites.movie_id == Movies.id).order_by(Movies.sentiment_trust.desc()).first()
    if not trusted:
        return "nothing in the favorites list"
    return f"Most trusted film: {trusted.title} | Trusted confiance: {trusted.sentiment_trust:.2f}"


"""
search smaller trusted film
"""
def smaller_trusted(username, db):
    user_id = get_user_id(username, db)
    trusted = db.query(Favorites.id, Favorites.added_at, Movies.title, Movies.sentiment, Movies.sentiment_trust).filter(Favorites.user_id == user_id).join(Movies, Favorites.movie_id == Movies.id).order_by(Movies.sentiment_trust.asc()).first()
    if not trusted:
        return "nothing in the favorites list"
    return f"Smaller trusted film: {trusted.title} | Trusted confiance: {trusted.sentiment_trust:.2f}"


"""
count all films
"""


def count_films(username, db):
    user_id = get_user_id(username, db)
    counted = db.query(Favorites.id, Favorites.added_at, Movies.title, Movies.sentiment, Movies.sentiment_trust).filter(Favorites.user_id == user_id).join(Movies, Favorites.movie_id == Movies.id).all()
    if not counted:
        return "nothing in the favorites list"
    return f"Count of films favs: {len(counted)}"

"""
first_added
"""
def first_added(username, db):
    user_id = get_user_id(username, db)
    trusted = db.query(Favorites.id, Favorites.added_at, Movies.title, Movies.sentiment, Movies.sentiment_trust).filter(Favorites.user_id == user_id).join(Movies, Favorites.movie_id == Movies.id).order_by(Favorites.added_at.asc()).first()
    if not trusted:
        return "nothing in the favorites list"
    return f"First film added on favorites: {trusted.title}"

"""
last_added
"""
def last_added(username, db):
    user_id = get_user_id(username, db)
    trusted = db.query(Favorites.id, Favorites.added_at, Movies.title, Movies.sentiment, Movies.sentiment_trust).filter(Favorites.user_id == user_id).join(Movies, Favorites.movie_id == Movies.id).order_by(Favorites.added_at.desc()).first()
    if not trusted:
        return "nothing in the favorites list"
    return f"Last film added on favorites: {trusted.title}"



"""
save on the chat history
"""
def save_chat(user_id, user_question, ai_response, db:Session) -> dict:
    chat = ChatHistory(user_id=user_id, user_question=user_question, ai_response=ai_response, chat_at=date.today())
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return {'message': 'chat saved!'}

"""
read last chat history msg
"""
def read_chat_history(user_id, db):
    history = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.chat_at.desc()).first()
    if not history:
        return {'ai_response': 'nothing history', 'user_question': 'nothing history'}
    return {'ai_response': history.ai_response, 'user_question': history.user_question}