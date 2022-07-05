from __future__ import annotations

import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    DateTime,
    func,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref, validates
from backend.database.base_class import Base


CASCADE_ALL_DELETE = "all, delete"


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)

    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sender_id = Column(Integer, ForeignKey("user.id"))
    receiver_id = Column(Integer, ForeignKey("user.id"))
