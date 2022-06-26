from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    DateTime,
    func,
    Boolean
)
from sqlalchemy.orm import relationship, backref
from backend.database.base_class import Base


CASCADE_ALL_DELETE = "all, delete"


users_groups = Table(
    "users_groups",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("group.id"), primary_key=True),
)


class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    users = relationship("User", secondary=users_groups, back_populates="groups")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


    def __str__(self):
        return self.name


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String(255),  nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    country = Column(String, nullable=True)
    address = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship("Role", backref=backref("user", lazy="joined"))
    groups = relationship("Group", secondary=users_groups, back_populates="users")


    def __repr__(self):
        return f"<User {self.username} {self.email}>"
