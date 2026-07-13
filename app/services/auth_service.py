from app.services.users_service import get_users_by_identifier, create_register_google
from app.auth import generate_token
from app.auth import pwd_context
from faker import Faker


def google_auth_service(token, db):
    
    user_info = token.get("userinfo") or {}
        # Extract user details
    email = user_info.get("email")  # Use email as username

    # Generate a JWT token with auth_method="google"
    user = get_users_by_identifier(email, db)
    access_token = generate_token(email, user.id)
    if not user:
        fake = Faker('pt_BR')
        password_criptografed = pwd_context.hash(fake.password(length=9, lower_case=True, upper_case=True, digits=True))
        user = create_register_google(db, email, email, password_criptografed)
        frontend_url = f'https://cinerag-analytics.vercel.app/google_register.html?token={access_token}'
        return frontend_url
    elif not user.is_profile_complete:
        frontend_url = f'https://cinerag-analytics.vercel.app/google_register.html?token={access_token}'
        return frontend_url

    
    
    
    frontend_url = f'https://cinerag-analytics.vercel.app/index.html?token={access_token}'
    return frontend_url