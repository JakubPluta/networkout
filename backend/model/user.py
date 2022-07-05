from __future__ import annotations
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
from sqlalchemy.orm import relationship, backref
from backend.database.base_class import Base
from .event import event_participants, Event
from .message import Message

CASCADE_ALL_DELETE = "all, delete"

users_groups = Table(
    "users_groups",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("group.id"), primary_key=True),
)

friendship = Table(
    "friendships",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), index=True),
    Column("friend_id", Integer, ForeignKey("user.id")),
    UniqueConstraint("user_id", "friend_id", name="unique_friendships"),
)


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    created_by_id = Column(Integer, ForeignKey("user.id"))
    created_by = relationship("User", backref=backref("user"))
    users = relationship("User", secondary=users_groups, back_populates="groups")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    users = relationship("User", back_populates="role")

    def __str__(self):
        return self.name

    @property
    def name_lower(self):
        return str(self.name).lower()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    country = Column(String, nullable=True)
    address = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    role_id = Column(Integer, ForeignKey("role.id"))
    role = relationship("Role", back_populates="users")

    groups = relationship("Group", secondary=users_groups, back_populates="users")

    friends = relationship(
        "User",
        secondary=friendship,
        primaryjoin=(id == friendship.c.user_id),
        secondaryjoin=(id == friendship.c.friend_id),
        backref=backref("friendships"),
    )

    events_joined = relationship(
        "Event", secondary=event_participants, back_populates="participants"
    )
    events_organized = relationship("Event", back_populates="host")

    messages_sent = relationship(
        "Message", backref="sender", primaryjoin=(id == Message.sender_id)
    )
    messages_received = relationship(
        "Message", backref="receiver", primaryjoin=(id == Message.receiver_id)
    )

    def __repr__(self):
        return f"<User {self.username} {self.email}>"

    def befriend(self, user: User):
        self.friends.append(user)
        user.friends.append(self)
        return self

    def unfriend(self, user: User):
        self.friends.remove(user)
        user.friends.remove(self)
        return self

    def is_friend(self, user: User):
        return user in self.friends
