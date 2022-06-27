import datetime
from typing import Optional
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    description: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    description: str


class RoleDB(BaseModel):
    id: Optional[int]
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True