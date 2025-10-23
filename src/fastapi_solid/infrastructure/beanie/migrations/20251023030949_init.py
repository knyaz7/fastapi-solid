from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import Field

from beanie import Document, iterative_migration


class OldPlayerOdm(Document):
    id: UUID = Field(default_factory=uuid4)  # type: ignore[reportIncompatibleVariableOverride]
    clor: str
    is_alive: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "players"


class NewPlayerOdm(Document):
    id: UUID = Field(default_factory=uuid4)  # type: ignore[reportIncompatibleVariableOverride]
    color: str
    is_alive: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "players"


class Forward:
    @iterative_migration()
    async def clor_to_color(
        self, input_document: OldPlayerOdm, output_document: NewPlayerOdm
    ):
        output_document.color = input_document.clor


class Backward:
    @iterative_migration()
    async def clor_to_color(
        self, input_document: NewPlayerOdm, output_document: OldPlayerOdm
    ):
        output_document.clor = input_document.color
