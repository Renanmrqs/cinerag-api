from app.models import Users
from app.models import Tokens
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.logging import logger

def add_token(db: Session, token: str):
    try:
        token_created = Tokens(token=token)
        db.add(token_created)
        db.commit()
        db.refresh(token_created)
        return token_created
    except Exception as e:
        logger.error(f"Add Token error: {e}")
        raise

def read_tokens(db: Session, token):
    return db.query(Tokens).where(Tokens.token == token).all()


# PEGAR TODOS USERS
def get_users(db: Session):
    return db.query(Users).all()

#retorna id do user
def get_user_id(name, db: Session):
    user = db.query(Users).filter(Users.username == name).first()
    return user.id

# busca user pelo nome
def get_users_by_identifier(identifier, db: Session):
    user = db.query(Users).filter(or_(Users.username == identifier, Users.email == identifier)).first()
    return user


# adiciona um user na tabela user
def create_register(db: Session, email, username, password):
    try:
        user = Users(email=email, username=username, password=password, is_profile_complete=True)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User registred - username: {username}")
        return user
    except Exception as e:
        logger.error(f"create register error: {e} | user: {username}")
        raise

def create_register_google(db: Session, email, username, password):
    try:  
        user = Users(email=email, username=username, password=password, is_profile_complete=False)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User google registred - email: {email}")
        return user
    except Exception as e:
        logger.error(f"create register google error: {e} | user: {username}")
        raise


def update_register(db: Session, username, password, id):
    try:
        user = db.query(Users).filter(Users.id == id).first()
        user.username = username
        user.password = password
        user.is_profile_complete = True
        db.commit()
        db.refresh(user)
        logger.info(f"User google update - email: {user.email} | username: {username}")
        return user
    except Exception as e:
        logger.error(f"update register error: {e} | user: {username}")
        raise
