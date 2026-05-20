from sqlalchemy import Integer, Column, ForeignKey, DateTime, BigInteger, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone, timedelta

### pegando a hora atual do brasil
fuso_br = timezone(timedelta(hours=-3))
def actual_hour():
    return datetime.now(fuso_br)

# MODELO BASE USANDO ORM E SQLALCHEMY
Base = declarative_base()

##
# MODELO PARA TABELA USERS
class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False) 
    username = Column(Text, nullable=False)

##
# MODELO PARA TABELA MOVIES
class Movies(Base):
    __tablename__ = "movies"
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    title = Column(Text, nullable=False)
    sentiment_score = Column(Integer, nullable=False)
    analyzed_at = Column(DateTime(timezone=True), default=actual_hour)
    


##
# MODELO PARA A TABELA FAVORITOS
class Favorites(Base):
    __tablename__ = 'favorites'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    movie_id = Column(BigInteger, ForeignKey("movies.id"), nullable=False)
    added_at = Column(DateTime(timezone=True), default=actual_hour)

##
# MODELO PARA A TABELA HISTORICO DE PESQUISAS
class SearchHistory(Base):
    __tablename__ = 'search_history'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    query = Column(Text, nullable=False)
    searched_at = Column(DateTime(timezone=True), default=actual_hour)

##
# MODELO PARA A TABELA CHAT HISTORY
class ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    user_question  = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False) 
    chat_at = Column(DateTime(timezone=True), default=actual_hour)
    


##
# MODELO PARA A TABELA TOKENS
class Tokens(Base):
    __tablename__ = 'expired_tokens'
    id = Column(BigInteger, primary_key=True)
    token = Column(Text, nullable=False, unique=True)