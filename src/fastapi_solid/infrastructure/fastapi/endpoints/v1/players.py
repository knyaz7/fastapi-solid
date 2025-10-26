from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache

from fastapi_solid.application.interfaces.common.pagination import Pagination
from fastapi_solid.application.players.dto import PlayerIn, PlayerOut, PlayerUpdate
from fastapi_solid.application.players.service import PlayerService
from fastapi_solid.infrastructure.di.container import Container
from fastapi_solid.infrastructure.fastapi.dependencies.pagination import get_pagination

players_router = APIRouter(prefix="/players", tags=["Players"])


@players_router.get("", response_model=list[PlayerOut])
@inject
async def get_players(
    player_service: Annotated[
        PlayerService, Depends(Provide[Container.player_service])
    ],
    pagination: Annotated[Pagination, Depends(get_pagination)],
):
    return await player_service.get_all(pagination)


@players_router.get("/{id}", response_model=PlayerOut)
@cache(10)  # caching http response
@inject
async def get_player(
    id: UUID,
    player_service: Annotated[
        PlayerService, Depends(Provide[Container.player_service])
    ],
):
    return await player_service.get_by_id(id)


@players_router.post("", response_model=PlayerOut, status_code=status.HTTP_201_CREATED)
@inject
async def create_player(
    player_in: PlayerIn,
    player_service: Annotated[
        PlayerService, Depends(Provide[Container.player_service])
    ],
):
    return await player_service.create(player_in)


@players_router.put("/{id}", response_model=PlayerOut)
@inject
async def update_player(
    id: UUID,
    player_update: PlayerUpdate,
    player_service: Annotated[
        PlayerService, Depends(Provide[Container.player_service])
    ],
):
    return await player_service.update(id, player_update)


@players_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_player(
    id: UUID,
    player_service: Annotated[
        PlayerService, Depends(Provide[Container.player_service])
    ],
):
    await player_service.delete(id)
