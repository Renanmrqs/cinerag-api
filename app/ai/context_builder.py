from google import genai
import os
from app.services.favorites import readl_all_films
from app.services.auth import get_user_id
from dotenv import load_dotenv
from app.services.chat import save_chat, read_chat_history
from app.ai.prompts import normal_prompt

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def context_builder(username, db):
    user_id = get_user_id(username, db)
    films = readl_all_films(user_id, db)
    chat_persistence = read_chat_history(user_id, db)
    return {"films": films, "chat_persistence": chat_persistence, "user_id": user_id}

def gemini_func(username, data, db):
    context = context_builder(username, db)
    
    
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        config={"system_instruction": normal_prompt(username, context)},
        contents= [                
                {"role": "user", "parts": [{"text": c for c in context['chat_persistence']['user_question']}]},
                {"role": "model", "parts": [{"text": c for c in context['chat_persistence']['ai_response']}]},                        
                {"role": "user", "parts": [{"text": data}]}]
    )
    save_chat(context["user_id"], data, response.text, db)
    return response.text
