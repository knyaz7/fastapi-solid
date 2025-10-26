from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache

from fastapi_solid.application.interfaces.common.pagination import Pagination
from fastapi_solid.application.users.dto import UserIn, UserOut, UserUpdate
from fastapi_solid.application.users.service import UserService
from fastapi_solid.infrastructure.di.container import Container
from fastapi_solid.infrastructure.fastapi.dependencies.pagination import get_pagination

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("", response_model=list[UserOut])
@inject
async def get_users(
    users_service: Annotated[UserService, Depends(Provide[Container.users_service])],
    pagination: Annotated[Pagination, Depends(get_pagination)],
):
    return await users_service.get_all(pagination)


# route to demonstrate our aside-cache
@users_router.get("/random", response_model=UserOut)  # not REST
@inject
async def get_random_user(
    users_service: Annotated[UserService, Depends(Provide[Container.users_service])],
):
    return await users_service.get_random()


@users_router.get("/{id}", response_model=UserOut)
@cache(10)  # caching http response
@inject
async def get_user(
    id: UUID,
    users_service: Annotated[UserService, Depends(Provide[Container.users_service])],
):
    return await users_service.get_by_id(id)


@users_router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user_in: UserIn,
    users_service: Annotated[UserService, Depends(Provide[Container.users_service])],
):
    return await users_service.create(user_in)


@users_router.put("/{id}", response_model=UserOut)
@inject
async def update_user(
    id: UUID,
    user_update: UserUpdate,
    users_service: Annotated[UserService, Depends(Provide[Container.users_service])],
):
    return await users_service.update(id, user_update)


@users_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_user(
    id: UUID,
    users_service: Annotated[UserService, Depends(Provide[Container.users_service])],
):
    await users_service.delete(id)
