from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserIn(BaseModel):
    name: str


class UserOut(UserIn):
    id: UUID
    created_at: datetime


class UserUpdate(UserIn):
    pass
