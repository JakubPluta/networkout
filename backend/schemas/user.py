import datetime
from typing import Optional, Sequence, List

from pydantic import BaseModel
from pydantic import EmailStr


class AddressBase(BaseModel):
    city: str
    country: str
    postal_code: Optional[str] = None
    street_name: Optional[str] = None
    street_number: Optional[str] = None


class AddressCreate(AddressBase):
    pass


class AddressFromDB(AddressBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class AddressFromDBFull(AddressFromDB):
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


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

    addresses: List[Optional[AddressFromDB]]

    class Config:
        orm_mode = True


class UsersList(BaseModel):
    results: Sequence[UserFromDB]
