from abc import ABC, abstractmethod
from uuid import UUID

from fastapi_solid.application.interfaces.common.pagination import Pagination
from fastapi_solid.application.players.dto import PlayerIn, PlayerUpdate
from fastapi_solid.domain.player.model import Player


class PlayerRepository(ABC):
    @abstractmethod
    async def get_all(self, pagination: Pagination | None = None) -> list[Player]: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Player | None: ...

    @abstractmethod
    async def create(self, player_in: PlayerIn) -> Player: ...

    @abstractmethod
    async def update(self, id: UUID, update_data: PlayerUpdate) -> Player: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
