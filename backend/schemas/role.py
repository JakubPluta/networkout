import datetime
from typing import Optional, Sequence, List
from pydantic import BaseModel
from enum import Enum


class RoleBase(BaseModel):
    name: str
    description: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]


class RoleDB(BaseModel):
    id: Optional[int]
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class RoleDBRead(BaseModel):
    id: Optional[int]
    name: str
    description: str

    class Config:
        orm_mode = True


class RolesList(BaseModel):
    results: Sequence[RoleDB]


class RoleEnum(str, Enum):
    admin: str = 'admin'
    test: str = 'test'
    user: str = 'user'