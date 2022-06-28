from backend.model.user import User, Group
from sqlalchemy.orm import Session
from backend import schemas


def get_all_groups(db: Session):
    return db.query(Group).all()


def get_group_by_id(db: Session, role_id: int) -> Group:
    return db.query(Group).filter(Group.id==role_id).first()


def get_group_by_name(db: Session, name: str):
    return db.query(Group).filter(Group.name == name).first()


def create_group(db: Session, role: schemas.GroupCreate, creator_id: int):
    create_data = role.dict()
    grp_db = Group(**create_data, created_by_id=creator_id)
    db.add(grp_db)
    db.commit()
    return grp_db