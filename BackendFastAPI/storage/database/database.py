from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DataBase as DB

SQLALCHEMY_DATABASE_URL = DB.URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL #, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
