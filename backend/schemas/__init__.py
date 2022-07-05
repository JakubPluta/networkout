from .user import *
from .role import *
from .group import *
from .event import *


class RoleDBUsers(BaseModel):
    id: Optional[int]
    name: str
    description: str
    users: Optional[Sequence[UserFromDB]]

    class Config:
        orm_mode = True


class GroupWithUsers(GroupDB):
    users: List[UserFromDBSmall]


class GroupList(BaseModel):
    results: Sequence[GroupWithUsers]

    class Config:
        orm_mode = True


class EventWithParticipants(EventDB):
    participants: List[UserFromDBSmall]


class EventsList(BaseModel):
    results: Sequence[EventWithParticipants]

    class Config:
        orm_mode = True
