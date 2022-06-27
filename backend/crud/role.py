from backend.model.user import User, Role
from sqlalchemy.orm import Session
from backend.security.hash_funcs import get_password_hash
from backend import schemas


def create_role(db: Session, role: schemas.RoleCreate):
    create_data = role.dict()
    role_db = Role(**create_data)
    db.add(role_db)
    db.commit()
    return role_db


def get_all_roles(db: Session):
    return db.query(Role).all()


def get_role_by_id(db: Session, role_id: int):
    return db.query(Role).filter(Role.id==role_id).first()


def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name_lower == name.lower()).first()