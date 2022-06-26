from backend.model.user import User, Address
import bcrypt
from sqlalchemy.orm import Session
# https://github.com/scionoftech/FastAPI-Full-Stack-Samples/blob/master/FastAPISQLAlchamy/app/crud/crud_users.py
from backend.security.hash_funcs import get_password_hash
from backend import schemas


def create_user(db: Session, user: schemas.UserCreate):
    create_data = user.dict()
    create_data.pop('password')
    user_db = User(**create_data)
    hashed_password = get_password_hash(user.password)
    user_db.hashed_password = hashed_password
    db.add(user_db)
    db.commit()
    return user_db


def update_user(db: Session, db_user: User, user: schemas.UserUpdate):
    user_from_db = db_user
    for field, value in user.dict().items():
        if field == 'password':
            setattr(user_from_db, 'hashed_password', get_password_hash(value))
        else:
            setattr(user_from_db, field, value)
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


def create_address(db: Session, address: schemas.AddressCreate):
    address_to_db: Address = \
        Address(
            city=address.city,
            country =address.country,
            postal_code =address.postal_code,
            street_name = address.street_number,
            street_number = address.street_number
    )



def create_address_for_user(db: Session, user: User, address: schemas.AddressCreate):
    address_to_db: Address = \
        Address(
            city=address.city,
            country =address.country,
            postal_code =address.postal_code,
            street_name = address.street_number,
            street_number = address.street_number
    )

    user.add_address(address_to_db)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_address_by_id(db: Session, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()


def get_user_address(db: Session, user_id: int):
    user = get_user(db, user_id)
    return user.addresses if user else None


