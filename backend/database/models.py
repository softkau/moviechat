from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

# SQLite 경로 지정 (상대경로 or 절대경로)
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/moviechat.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def current_time():
    return datetime.now(timezone.utc)

# TABLE 이름(요구사항 명세서_6조.pdf p. 18 참조)
TABLE_USER              = "users"
TABLE_MOVIE             = "movies"
TABLE_BOOKMARKED_MOVIE  = "bookmarked_movies"
TABLE_ARCHIVED_MOVIE    = "archived_movies"
TABLE_CHAT_ROOM         = "chat_rooms"
TABLE_CHAT_HISTORY      = "chat_history"
TABLE_CHARACTER_PROFILE = "character_profiles"
TABLE_DIRECTOR          = "directors"
TABLE_GENRE             = "genres"
TABLE_ACTOR             = "actors"
TABLE_PLATFORM          = "platforms"
REL_MOVIE_GENRE         = "rel_movie_genres"
REL_MOVIE_ACTOR         = "rel_movie_actors"
REL_MOVIE_PLATFORM      = "rel_movie_platforms"

def fk(tablename: str) -> str: return f"{tablename}.id"

class User(Base):
    __tablename__ = TABLE_USER
    id       = Column(Integer,    primary_key=True, index=True)
    email      = Column(String,   nullable=False,   unique=True)
    password   = Column(String,   nullable=False)
    nickname   = Column(String,   nullable=False)
    created_at = Column(DateTime, default=current_time)

class Movie(Base):
    __tablename__ = TABLE_MOVIE
    id              = Column(Integer,  primary_key=True, index=True)
    overview        = Column(String,   nullable=True)
    release_date    = Column(Date,     nullable=True)
    poster_img_url  = Column(String,   nullable=True)
    trailer_img_url = Column(String,   nullable=True)
    director_id     = Column(Integer,  ForeignKey(fk(TABLE_DIRECTOR)), nullable=True)

class BookmarkedMovie(Base):
    __tablename__ = TABLE_BOOKMARKED_MOVIE
    movie_id      = Column(Integer, ForeignKey(fk(TABLE_MOVIE)), primary_key=True)
    user_id       = Column(Integer, ForeignKey(fk(TABLE_USER)),  primary_key=True)
    created_at    = Column(DateTime, default=current_time)
    
class ArchivedMovie(Base):
    __tablename__ = TABLE_ARCHIVED_MOVIE
    movie_id      = Column(Integer, ForeignKey(fk(TABLE_MOVIE)), primary_key=True)
    user_id       = Column(Integer, ForeignKey(fk(TABLE_USER)),  primary_key=True)
    rating        = Column(Integer, nullable=False)
    created_at    = Column(DateTime, default=current_time)
    
class Director(Base):
    __tablename__ = TABLE_DIRECTOR
    id   = Column(Integer, primary_key=True)
    name = Column(String,  nullable=False)
    
class ChatRoom(Base):
    __tablename__ = TABLE_CHAT_ROOM
    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey(fk(TABLE_USER)), nullable=False)
    character_id  = Column(Integer, ForeignKey(fk(TABLE_CHARACTER_PROFILE)))
    created_at    = Column(DateTime, default=current_time)
    
class ChatHistory(Base):
    __tablename__ = TABLE_CHAT_HISTORY
    id = Column(Integer, primary_key=True, index=True)
    room_id   = Column(Integer, ForeignKey(fk(TABLE_CHAT_ROOM)))
    ai_chat   = Column(String, nullable=False) # message => ai_chat   ; refactored. AI 응답과 user 요청을 하나로 두는게 더 simple하다
    user_chat = Column(String, nullable=False) # message => user_chat ;
    timestamp = Column(DateTime, nullable=False)
    
class CharacterProfile(Base):
    __tablename__ = TABLE_CHARACTER_PROFILE
    id = Column(Integer, primary_key=True, index=True)
    movie_id       = Column(Integer, ForeignKey(fk(TABLE_MOVIE)), nullable=False)
    name           = Column(String, nullable=False)
    description    = Column(String, nullable=False)
    tone           = Column(String, nullable=False)
    other_features = Column(String, nullable=True)
    
class Genre:
    __tablename__ = TABLE_GENRE
    id   = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
class Actor:
    __tablename__ = TABLE_ACTOR
    id   = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Platfrom:
    __tablename__ = TABLE_PLATFORM
    id   = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class MovieGenre:
    __tablename__ = REL_MOVIE_GENRE
    movie_id = Column(Integer, ForeignKey(fk(TABLE_MOVIE)), nullable=False)
    genre_id = Column(Integer, ForeignKey(fk(TABLE_GENRE)), nullable=False)

class MovieActor:
    __tablename__ = REL_MOVIE_ACTOR
    movie_id = Column(Integer, ForeignKey(fk(TABLE_MOVIE)), nullable=False)
    actor_id = Column(Integer, ForeignKey(fk(TABLE_ACTOR)), nullable=False)

class MoviePlatform:
    __tablename__ = REL_MOVIE_PLATFORM
    movie_id    = Column(Integer, ForeignKey(fk(TABLE_MOVIE)), nullable=False)
    platform_id = Column(Integer, ForeignKey(fk(TABLE_PLATFORM)), nullable=False)
