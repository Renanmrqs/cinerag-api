from google import genai
import os
from app.services.favorites import readl_all_films
from app.services.auth import get_user_id
from dotenv import load_dotenv
from app.services.chat import save_chat, read_chat_history

load_dotenv()

print(os.getenv("GEMINI_API_KEY"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def gemini_func(username, data, db):
    user_id = get_user_id(username, db)
    films = readl_all_films(user_id, db)
    chat_persistence = read_chat_history(user_id, db)
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        config={"system_instruction": f"You are a consultant for a cinerag analytics, your name is CineAI, based on the user's favorite movies: {films} you must answer the given instructions for this user {username}. A short answer and enjoyed"},
        contents = [
                {"role": "user", "parts": [{"text": chat_persistence['user_question']}]},
                {"role": "model", "parts": [{"text": chat_persistence['ai_response']}]},
                {"role": "user", "parts": [{"text": data}]}]
    )
    save_chat(user_id, data, response.text, db)
    return response.text


