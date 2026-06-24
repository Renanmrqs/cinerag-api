from sqlalchemy import Integer, Column, ForeignKey, DateTime, BigInteger, Text, text, CheckConstraint, Float, Boolean, UniqueConstraint
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone, timedelta
import enum

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
    username = Column(Text, nullable=False, unique=True)
    is_profile_complete = Column(Boolean, default=True, server_default=text('true'), nullable=False)

##
# MODELO PARA TABELA MOVIES
class Movies(Base):
    __tablename__ = "movies"
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    title = Column(Text, nullable=False)
    sentiment_trust = Column(Float, nullable=False)
    sentiment = Column(Text, nullable=False)
    analyzed_at = Column(DateTime(timezone=True), default=actual_hour)
    has_reviews =  Column(Boolean, default=True)
    __table_args__ = (
    CheckConstraint("sentiment IN ('positive', 'negative', 'mixed')", name="check_sentiment_valid"),
    )
    


##
# MODELO PARA A TABELA FAVORITOS
class Favorites(Base):
    __tablename__ = 'favorites'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    movie_id = Column(BigInteger, ForeignKey("movies.id"), nullable=False)
    added_at = Column(DateTime(timezone=True), default=actual_hour)
    
    __table_args__ = (
        UniqueConstraint(user_id, movie_id),
    )


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

##
# MODELO PARA A TABELA GENEROS
class Genres(Base):
    __tablename__ = 'genres'
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(Text, nullable=False)

##
# MODELO PARA A TABELA DE PREFENCIAS DO USUARIO
class UserPreferences(Base):
    __tablename__ = 'user_preferences'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    genre_id = Column(BigInteger, ForeignKey("genres.id"), nullable=False)
    score = Column(BigInteger, nullable=False)

    __tableargs__ = (
        CheckConstraint("score >= 0", name="check_score_minimun" )
    )
    
