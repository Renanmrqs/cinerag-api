from app.models import Users
from app.models import Tokens
from sqlalchemy.orm import Session
from sqlalchemy import or_

def add_token(db: Session, token: str):
    token_created = Tokens(token=token)
    db.add(token_created)
    db.commit()
    db.refresh(token_created)
    return token_created

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
    user = Users(email=email, username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_register(db: Session, username, password, email):
    user = db.query(Users).filter(Users.email == email).first()
    user.username = username
    user.password = password
    db.commit()
    db.refresh(user)
    return user