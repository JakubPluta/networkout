from __future__ import annotations
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    DateTime,
    func,
    Boolean, UniqueConstraint
)
from sqlalchemy.orm import relationship, backref
from backend.database.base_class import Base


CASCADE_ALL_DELETE = "all, delete"

event_participants = Table(
    "event_participants",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("event.id"), primary_key=True),
)



class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    address = Column(String,nullable=False)
    date = Column(DateTime, nullable=False)

    host_id = Column(Integer, ForeignKey('user.id'))
    host = relationship("User")

    participants = relationship(
        'User', secondary=event_participants, back_populates='events_joined'
    )