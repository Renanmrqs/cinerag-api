from authlib.integrations.starlette_client import OAuth
import os
from fastapi import Depends, Request, APIRouter
from fastapi.responses import RedirectResponse
from datetime import timedelta
from dotenv import load_dotenv
from app.database import get_db
from sqlalchemy.orm import Session

load_dotenv()

router = APIRouter()

oauth = OAuth
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
    return await oauth.google.authorize_redirect(request, redirect_url="http://localhost:8000/auth/google/callback")

@router.get("/auth/google/callback", tags=["auth"])
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo") or {}

        # Extract user details
        username = user_info.get("email")  # Use email as username

        # Generate a JWT token with auth_method="google"
        access_token = create_access_token(
            settings, 
            data={"sub": username}, 
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            auth_method="google"
        )

        return {"access_token": access_token, "token": token}
    except Exception as e:
        import traceback
        print("Error:", traceback.format_exc())  # Debugging step
        return {"error": str(e)}