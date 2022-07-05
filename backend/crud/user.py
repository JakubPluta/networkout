from backend.model.user import User, Role
import bcrypt
from sqlalchemy.orm import Session

# https://github.com/scionoftech/FastAPI-Full-Stack-Samples/blob/master/FastAPISQLAlchamy/app/crud/crud_users.py
from backend.security.hash_funcs import get_password_hash
from backend import schemas
from backend.utils.exc import FriendshipException


def create_user(db: Session, user: schemas.UserCreate):
    create_data = user.dict()
    create_data.pop("password")
    user_db = User(**create_data)
    hashed_password = get_password_hash(user.password)
    user_db.hashed_password = hashed_password
    db.add(user_db)
    db.commit()
    return user_db


def create_user_with_role(db: Session, user: schemas.UserCreateAdminView):
    create_data = user.dict()
    create_data.pop("password")
    user_db = User(**create_data)
    hashed_password = get_password_hash(user.password)
    user_db.hashed_password = hashed_password
    db.add(user_db)
    db.commit()
    return user_db


def update_user(db: Session, db_user: User, user: schemas.UserUpdate):
    user_from_db = db_user
    for field, value in user.dict().items():
        if field == "password":
            setattr(user_from_db, "hashed_password", get_password_hash(value))
        else:
            setattr(user_from_db, field, value)
    db.add(user_from_db)
    db.commit()
    db.refresh(user_from_db)
    return user_from_db


def grant_superuser_permissions(
    db: Session, db_user: User, user: schemas.UserSuperUserUpdate
):
    user_from_db = db_user
    user_from_db.is_superuser = user.is_superuser
    db.add(user_from_db)
    db.commit()
    db.refresh(user_from_db)
    return user_from_db


def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
    db.refresh(db_user)
    return True


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


def become_friend_with_user(db: Session, user: User, other_user: User):
    try:
        user.befriend(other_user)
        db.add_all([user, other_user])
        db.commit()
        db.refresh(user)
    except Exception as e:
        raise FriendshipException(f"{user} is already friend with {other_user}") from e
    return user


def unfriend_with_user(db: Session, user: User, other_user: User):
    try:
        user.unfriend(other_user)
        db.add_all([user, other_user])
        db.commit()
        db.refresh(user)
    except Exception as e:
        raise FriendshipException(f"{user} is are not friend with {other_user}") from e
    return user


def get_my_friends(user: User):
    return user.friends
