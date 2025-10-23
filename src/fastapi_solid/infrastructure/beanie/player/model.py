from datetime import UTC, datetime
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field


class PlayerOdm(Document):
    id: UUID = Field(default_factory=uuid4)  # type: ignore[reportIncompatibleVariableOverride]
    color: str
    is_alive: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "players"
