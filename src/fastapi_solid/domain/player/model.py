from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Player:
    id: UUID
    color: str
    is_alive: bool
    created_at: datetime
