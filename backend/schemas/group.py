import datetime
from typing import Optional, List, Sequence
from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str
    description: str


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    description: str


class GroupDB(BaseModel):
    id: Optional[int]
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


