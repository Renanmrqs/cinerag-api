from app.services.favorites_service import readl_all_films, read_genres_user
from app.services.users_service import get_user_id
from app.services.querys_service import save_chat, read_chat_history


def context_builder(username, db):
    user_id = get_user_id(username, db)
    films = readl_all_films(user_id, db)
    genres_preferences = read_genres_user(user_id, db)
    chat_persistence = read_chat_history(user_id, db)
    return {"films": films, "chat_persistence": chat_persistence, "genres_preferences": genres_preferences, "user_id": user_id}


