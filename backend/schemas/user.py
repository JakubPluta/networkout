import datetime
from typing import Optional, Sequence, List

from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str
    password: str


class UserFromDB(UserBase):
    id: int
    is_superuser: bool
    is_active: bool
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    role_id: Optional[int]

    class Config:
        orm_mode = True


class UsersList(BaseModel):
    results: Sequence[UserFromDB]
