import datetime
from typing import Optional, Sequence
from pydantic import BaseModel
from pydantic import EmailStr
from .role import RoleDBRead


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserCreateAdminView(UserBase):
    password: str
    is_superuser: bool = True
    role_id: Optional[int]


class UserUpdate(BaseModel):
    username: str
    password: str


class UserFromDB(UserBase):
    id: int
    is_superuser: bool
    is_active: bool
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    role: Optional[RoleDBRead]

    class Config:
        orm_mode = True


class UsersList(BaseModel):
    results: Sequence[UserFromDB]
