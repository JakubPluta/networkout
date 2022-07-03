import datetime
from typing import Optional, List, Sequence
from pydantic import BaseModel


class EventBase(BaseModel):
    name: str
    description: str
    address: str
    date: datetime.datetime


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: str
    description: str
    address: str
    date: datetime.datetime


class EventDB(EventBase):
    id: Optional[int]
    host_id: Optional[int]

    class Config:
        orm_mode = True


class EventsList(BaseModel):
    results: Sequence[EventDB]

    class Config:
        orm_mode = True
