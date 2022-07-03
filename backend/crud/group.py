from backend.model.user import User, Group
from sqlalchemy.orm import Session
from backend import schemas
from logging import getLogger


log = getLogger(__name__)


def get_all_groups(db: Session):
    return db.query(Group).all()


def get_group_by_id(db: Session, group_id: int) -> Group:
    return db.query(Group).filter(Group.id == group_id).first()


def get_group_by_name(db: Session, name: str):
    return db.query(Group).filter(Group.name == name).first()


def create_group(db: Session, group: schemas.GroupCreate, creator_id: int):
    create_data = group.dict()
    grp_db = Group(**create_data, created_by_id=creator_id)
    db.add(grp_db)
    db.commit()
    return grp_db


def delete_group(db: Session, group: Group):
    db.delete(group)
    db.commit()
    return group


def add_user_to_group(db: Session, user: User, group_id: int):
    group = get_group_by_id(db, group_id)
    group.users.append(user)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def remove_user_from_group(group: Group,  user: User):
    try:
        group.users.pop(user)
    except ValueError as e:
        log.warning(f"User not in group {str(e)}")
    return group


def is_user_in_group(db: Session, user: User, group_id: int):
    group = get_group_by_id(db, group_id)
    return user in group.users

