from app.ai.context_builder import context_builder
from app.ai.prompts import normal_prompt
from google import genai
import os
from dotenv import load_dotenv
from app.services.querys_service import save_chat

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


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