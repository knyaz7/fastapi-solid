from uuid import UUID

from fastapi_solid.application.exceptions.app_error import NotFound, ValidationError
from fastapi_solid.application.interfaces.common.pagination import Pagination
from fastapi_solid.application.interfaces.common.uow import UnitOfWork
from fastapi_solid.application.interfaces.players.repo import PlayerRepository
from fastapi_solid.application.players.dto import PlayerIn, PlayerOut, PlayerUpdate
from fastapi_solid.domain.player.model import Player
from fastapi_solid.domain.player.rules import can_add_player
from fastapi_solid.utils.logging.logger import get_logger

logger = get_logger(__name__)


class PlayerService:
    def __init__(self, uow: UnitOfWork, players_repo: PlayerRepository):
        self.uow = uow
        self.players_repo = players_repo

    async def get_all(self, pagination: Pagination) -> list[PlayerOut]:
        async with self.uow:
            players = await self.players_repo.get_all(pagination)
            return [PlayerOut.model_validate(p, from_attributes=True) for p in players]

    async def get_by_id(self, player_id: UUID) -> PlayerOut:
        async with self.uow:
            player = await self.players_repo.get_by_id(player_id)
            if not player:
                raise NotFound.domain_entity(Player, player_id)
            return PlayerOut.model_validate(player, from_attributes=True)

    async def create(self, player_in: PlayerIn) -> PlayerOut:
        if not can_add_player(player_in.color):
            raise ValidationError(
                f"Player with color '{player_in.color}' cannot be added"
            )
        async with self.uow as unit_of_work:
            player = await self.players_repo.create(player_in)
            await unit_of_work.commit()
        return PlayerOut.model_validate(player, from_attributes=True)

    async def update(self, player_id: UUID, update_data: PlayerUpdate) -> PlayerOut:
        async with self.uow as unit_of_work:
            player = await self.players_repo.update(player_id, update_data)
            await unit_of_work.commit()
        return PlayerOut.model_validate(player, from_attributes=True)

    async def delete(self, player_id: UUID) -> None:
        async with self.uow as unit_of_work:
            await self.players_repo.delete(player_id)
            await unit_of_work.commit()
