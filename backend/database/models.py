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

class User(Base):
    __tablename__ = "users"
    id       = Column(Integer,    primary_key=True, index=True)
    email      = Column(String,   nullable=False,   unique=True)
    password   = Column(String,   nullable=False)
    nickname   = Column(String,   nullable=False)
    created_at = Column(DateTime, default=current_time)

class Movie(Base):
    __tablename__ = "movies"
    id              = Column(Integer,  primary_key=True, index=True)
    overview        = Column(String,   nullable=True)
    release_date    = Column(Date,     nullable=True)
    poster_img_url  = Column(String,   nullable=True)
    trailer_img_url = Column(String,   nullable=True)
    director_id     = Column(Integer,  ForeignKey("directors.id"), nullable=True)

class BookmarkedMovie(Base):
    __tablename__ = "bookmarked_movies"
    movie_id = Column(Integer, ForeignKey("Movie.id"), primary_key=True)
    user_id  = Column(Integer, ForeignKey("User.id"),  primary_key=True)
    created_at = Column(DateTime, default=current_time)
    
class ArchivedMovie(Base):
    __tablename__ = "archived_movies"
    movie_id = Column(Integer, ForeignKey("Movie.id"), primary_key=True)
    user_id  = Column(Integer, ForeignKey("User.id"),  primary_key=True)
    created_at = Column(DateTime, default=current_time)
    
    