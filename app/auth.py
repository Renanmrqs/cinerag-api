import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def generate_token(username, user_id):
    timestampe = datetime.now(timezone.utc) + timedelta(hours=2)
    dictionary_user = {"sub": str(user_id), 'username': username, "exp": timestampe}
    token = jwt.encode(dictionary_user, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    
        username = payload.get("sub")
        if username is None: 
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail=f"O token enviado está num formato inválido.")
    
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired time.")
    
    except jwt.PyJWKError:
        raise HTTPException(status_code=401, detail="Invalid user.")