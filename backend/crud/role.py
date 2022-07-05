from backend.model.user import User, Role
from sqlalchemy.orm import Session
from backend import schemas


def create_role(db: Session, role: schemas.RoleCreate):
    create_data = role.dict()
    role_db = Role(**create_data)
    db.add(role_db)
    db.commit()
    return role_db


def update_role(db: Session, role_db: Role, role_update: schemas.RoleUpdate):
    role_dict = role_update.dict(exclude_unset=True)
    for field, value in role_dict.items():
        setattr(role_db, field, value)
    db.add(role_db)
    db.commit()
    db.refresh(role_db)
    return role_db


def get_all_roles(db: Session):
    return db.query(Role).all()


def delete_role(db: Session, role_id: int):
    role = get_role_by_id(db, role_id)
    if not role:
        return None
    db.delete(role)
    db.commit()


def get_role_by_id(db: Session, role_id: int) -> Role:
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()


def add_role_to_user(db: Session, user: User, role_id: int):
    role = get_role_by_id(db, role_id)
    if not role:
        return None
    role.users.append(user)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role
