from backend.model.user import User, Event
from sqlalchemy.orm import Session
from backend import schemas
from logging import getLogger
from backend.utils.exc import EventException

log = getLogger(__name__)


def create_event(db: Session, event: schemas.EventCreate, host_id: int):
    event_data = event.dict()
    event_db: Event = Event(**event_data, host_id=host_id)
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db


def delete_event(db: Session, event: Event):
    db.delete(event)
    db.commit()
    return event


def get_all_events(db: Session):
    return db.query(Event).all()


def get_event_by_id(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()


def get_event_by_name(db: Session, event_name: str):
    return db.query(Event).filter(str(Event.name).lower() == event_name.lower()).first()


def join_event(db: Session, user: User, event: Event):
    if user not in event.participants:
        event.participants.append(user)
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
    raise EventException(f"User {user.id} already participate in event {event.name}")


def quit_event(db: Session, user: User, event: Event):
    if user in event.participants:
        event.participants.remove(user)
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
    raise EventException(f"User {user.id} not participate in event {event.name}")


def get_event_participates(event: Event):
    return event.participants
