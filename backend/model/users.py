from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    DateTime,
    func,
    Text,
)
from sqlalchemy.orm import relationship, backref
from backend.database import Base, engine, meta

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

profile_hobbies = Table(
    "profile_hobbies",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey("profile.id")),
    Column("hobby_id", Integer, ForeignKey("hobby.id")),
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

    _password = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    addresses = relationship("Address", secondary=user_address, back_populates="users")
    roles = relationship("Role", secondary=user_role, backref=backref("users", lazy="joined"))

    profile = relationship("Profile",  back_populates='user',  uselist=False, cascade=CASCADE_ALL_DELETE)

    def __repr__(self):
        return f"<User {self.username} {self.email}>"

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if len(value) < 6:
            raise Exception("Password should be minimum 6 character long")
        self._password = value


class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("user.id"))

    bio = Column(Text, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    phone_number = Column(String, nullable=True)
    picture = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates='profile')

    hobbies = relationship("Hobby", back_populates='profiles', secondary=profile_hobbies)


class Hobby(Base):
    __tablename__ = "hobby"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    profiles = relationship("Profile", back_populates='hobbies', secondary=profile_hobbies)


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
