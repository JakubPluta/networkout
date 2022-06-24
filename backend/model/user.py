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

user_address = Table(
    "user_address",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("address_id", Integer, ForeignKey("address.id"), primary_key=True),
)


user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
)


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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    addresses = relationship("Address", secondary=user_address, back_populates="users")
    roles = relationship("Role", secondary=user_role, backref=backref("users", lazy="joined"))

    def __repr__(self):
        return f"<User {self.username} {self.email}>"


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    postal_code = Column(String, nullable=True)
    street_name = Column(String, nullable=True)
    street_number = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    users = relationship("User", secondary=user_address, back_populates="addresses")

    def __repr__(self):
        return f"<Address {self.city} {self.street_name} {self.street_number}>"
