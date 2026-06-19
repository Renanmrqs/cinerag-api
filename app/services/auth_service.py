from app.services.users_service import get_users_by_identifier, create_register_google
from app.auth import generate_token

def google_auth_service(token, db):
    
    user_info = token.get("userinfo") or {}
        # Extract user details
    email = user_info.get("email")  # Use email as username

    # Generate a JWT token with auth_method="google"
    user = get_users_by_identifier(email, db)
    
    if not user:
        user = create_register_google(db, email, email, "google_oauth")
        access_token = generate_token(email, user.id)
        frontend_url = f'https://cinerag-analytics.vercel.app/google_register.html?token={access_token}'
        return frontend_url
    
    access_token = generate_token(email, user.id)
    
    frontend_url = f'https://cinerag-analytics.vercel.app/index.html?token={access_token}'
    return frontend_url