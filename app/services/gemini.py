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

    print(chat_persistence)
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        config={"system_instruction": f"You are CineAI, a film consultant for CineRAG Analytics. The user's name is {username} and their favorite films are: {films}. Be concise, enthusiastic and personal. Never recommend a film already in the user's favorites list. Never repeat a recommendation already made in this conversation. Base your recommendations on the emotional and thematic profile of the user's favorites."},
        contents= [
                # [c for c in user_list],
                # [m for m in model_list],
                
                {"role": "user", "parts": [{"text": c for c in chat_persistence['user_question']}]},
                {"role": "model", "parts": [{"text": c for c in chat_persistence['ai_response']}]},                        
                {"role": "user", "parts": [{"text": data}]}]
    )
    save_chat(user_id, data, response.text, db)
    return response.text


