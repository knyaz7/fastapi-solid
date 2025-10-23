from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PlayerIn(BaseModel):
    color: str
    is_alive: bool


class PlayerOut(PlayerIn):
    id: UUID
    created_at: datetime


class PlayerUpdate(PlayerIn):
    pass
