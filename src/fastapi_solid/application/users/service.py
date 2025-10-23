from uuid import UUID

from fastapi_solid.application.exceptions.app_error import NotFound
from fastapi_solid.application.interfaces.common.pagination import Pagination
from fastapi_solid.application.interfaces.common.uow import UnitOfWork
from fastapi_solid.application.interfaces.users.repo import UserRepository
from fastapi_solid.application.users.dto import UserIn, UserOut, UserUpdate
from fastapi_solid.domain.user.model import User
from fastapi_solid.utils.logging.logger import get_logger

logger = get_logger(__name__)


class UserService:
    def __init__(self, uow: UnitOfWork, users_repo: UserRepository):
        self.uow = uow
        self.users_repo = users_repo

    async def get_all(self, pagination: Pagination) -> list[UserOut]:
        async with self.uow:
            users = await self.users_repo.get_all(pagination)
            return [UserOut.model_validate(u, from_attributes=True) for u in users]

    async def get_by_id(self, user_id: UUID) -> UserOut:
        async with self.uow:
            user = await self.users_repo.get_by_id(user_id)
            if not user:
                raise NotFound.domain_entity(User, user_id)
            return UserOut.model_validate(user, from_attributes=True)

    async def get_random(self) -> UserOut:
        async with self.uow:
            user = await self.users_repo.get_random_user()
            if not user:
                raise NotFound("No users to select from")
            return UserOut.model_validate(user, from_attributes=True)

    async def create(self, user_in: UserIn) -> UserOut:
        async with self.uow as unit_of_work:
            user = await self.users_repo.create(user_in)
            await unit_of_work.commit()
        return UserOut.model_validate(user, from_attributes=True)

    async def update(self, user_id: UUID, update_data: UserUpdate) -> UserOut:
        async with self.uow as unit_of_work:
            user = await self.users_repo.update(user_id, update_data)
            await unit_of_work.commit()
        return UserOut.model_validate(user, from_attributes=True)

    async def delete(self, user_id: UUID) -> None:
        async with self.uow as unit_of_work:
            await self.users_repo.delete(user_id)
            await unit_of_work.commit()
