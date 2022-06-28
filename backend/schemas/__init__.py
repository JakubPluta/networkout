from .user import *
from .role import *


class RoleDBUsers(BaseModel):
    id: Optional[int]
    name: str
    description: str
    users: Optional[Sequence[UserFromDB]]

    class Config:
        orm_mode = True

