from backend.model.user import User
import bcrypt
from sqlalchemy.orm import Session
# https://github.com/scionoftech/FastAPI-Full-Stack-Samples/blob/master/FastAPISQLAlchamy/app/crud/crud_users.py
from backend.security.auth import AuthHandler as AH
from backend import schemas


def create_user(db: Session, user: schemas.UserCreate):
    create_data = user.dict()
    create_data.pop('password')
    user_db = User(**create_data)
    hashed_password = AH.get_password_hash(user.password)
    user_db.hashed_password = hashed_password
    db.add(user_db)
    db.commit()
    return user_db


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_all_users(db: Session):
    return db.query(User).all()


def is_superuser(db: Session, user_id: int) -> bool:
    usr = get_user(db, user_id)
    superuser = False
    if usr:
        superuser = usr.is_superuser
    return superuser
