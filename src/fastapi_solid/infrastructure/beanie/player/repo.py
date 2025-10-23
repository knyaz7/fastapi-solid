from uuid import UUID

from fastapi_solid.application.interfaces.common.pagination import Pagination
from fastapi_solid.application.interfaces.players.repo import PlayerRepository
from fastapi_solid.application.players.dto import PlayerIn, PlayerUpdate
from fastapi_solid.domain.player.model import Player
from fastapi_solid.infrastructure.beanie.player.model import PlayerOdm
from fastapi_solid.infrastructure.beanie.setup.base_repo import BeanieRepo
from fastapi_solid.utils.converters.beanie_to_dc import to_dataclass


class BeaniePlayerRepo(PlayerRepository, BeanieRepo[PlayerOdm]):
    model = PlayerOdm

    async def get_all(self, pagination: Pagination | None = None) -> list[Player]:
        docs = await self._get_all(pagination)
        return [to_dataclass(d, Player) for d in docs]

    async def get_by_id(self, id: UUID) -> Player | None:
        doc = await self._get_by_id(id)
        return to_dataclass(doc, Player) if doc else None

    async def create(self, player_in: PlayerIn) -> Player:
        doc = await self._create(player_in.model_dump())
        return to_dataclass(doc, Player)

    async def update(self, id: UUID, update_data: PlayerUpdate) -> Player:
        result = await self._update_by_id(id, update_data.model_dump())
        return to_dataclass(result, Player)

    async def delete(self, id: UUID) -> None:
        await self._delete(id)
