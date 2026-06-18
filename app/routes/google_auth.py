from authlib.integrations.starlette_client import OAuth
import os
from fastapi import Depends, Request, APIRouter
from fastapi.responses import RedirectResponse
from datetime import timedelta
from dotenv import load_dotenv
from app.database import get_db
from sqlalchemy.orm import Session
from app.auth import generate_token
from app.services.users_service import get_users_by_identifier, create_register_google

load_dotenv()

router = APIRouter()

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.environ['GOOGLE_CLIENT_ID'],
    client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration"
)

@router.get("/auth/google", tags=["auth"])
async def auth_google(request: Request):
    return await oauth.google.authorize_redirect(request, redirect_uri="https://cinerag-api.onrender.com/auth/google/callback")

@router.get("/auth/google/callback", tags=["auth"])
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo") or {}

        # Extract user details
        email = user_info.get("email")  # Use email as username

        # Generate a JWT token with auth_method="google"
        user = get_users_by_identifier(email, db)
        
        if not user:
            user = create_register_google(db, email, email, "google_oauth")
            access_token = generate_token(email, user.id)
            frontend_url = f'https://cinerag-analytics.vercel.app/google_register.html?token={access_token}'
            return RedirectResponse(url=frontend_url)
        access_token = generate_token(email, user.id)
        
        frontend_url = f'https://cinerag-analytics.vercel.app/index.html?token={access_token}'
        return RedirectResponse(url=frontend_url)
    except Exception as e:
        import traceback
        print("Error:", traceback.format_exc())  # Debugging step
        return {"error": str(e)}