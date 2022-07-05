from backend.database.db import get_db
from backend.crud import user as user_crud
from backend.model.user import User
from backend.model.message import Message
from sqlalchemy.orm import Session
from backend import schemas
from logging import getLogger


log = getLogger(__name__)


def get_all_messages(db: Session):
    return db.query(Message).all()


def get_message_by_id(db: Session, msg_id: int) -> Message:
    return db.query(Message).filter(Message.id == msg_id).first()


def get_all_messages_send_by_user_id(db: Session, user_id: int):
    msg = db.query(Message).filter(Message.sender_id == user_id).first()
    return msg


def create_message(db: Session, current_user_id: int, to_user_id: int, content: str):
    receiver = user_crud.get_user(db, to_user_id)
    if receiver is None:
        raise Exception
    msg = Message(
        content=content,
        sender_id=current_user_id,
        receiver_id=to_user_id,
    )

    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
