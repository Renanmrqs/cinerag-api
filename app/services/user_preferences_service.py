from app.models import UserPreferences
from sqlalchemy.orm import Session

def add_user_preferences(genre_id, user_id, db: Session):
    genre = db.query(UserPreferences).filter(
        UserPreferences.user_id == user_id,
        UserPreferences.genre_id == genre_id
    ).first()

    if genre:
        genre.score += 1
    else:
        new_genre = UserPreferences(user_id=user_id, genre_id=genre_id, score=1)
        db.add(new_genre)

def del_user_preferences(genre_id, user_id, db: Session):
    genre = db.query(UserPreferences).filter(
        UserPreferences.user_id == user_id,
        UserPreferences.genre_id == genre_id
    ).first()
    if genre:
        if genre.score > 1:
            genre.score -= 1
        else:
            genre.score = 0
