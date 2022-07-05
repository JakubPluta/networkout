from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import settings


# TODO: Replace with postgres, add dockerfile
SQLALCHEMY_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)
SessionLocal: sessionmaker = sessionmaker(
    bind=engine, autocommit=False, autoflush=False
)
