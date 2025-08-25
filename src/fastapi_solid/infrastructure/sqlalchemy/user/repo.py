import random
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_solid.application.exceptions.app_error import NotFound
from fastapi_solid.application.interfaces.common.key_value_cache import KeyValueCache
from fastapi_solid.application.interfaces.common.pagination import Pagination
from fastapi_solid.application.interfaces.users.repo import UserRepository
from fastapi_solid.application.users.dto import UserIn, UserUpdate
from fastapi_solid.domain.user.model import User
from fastapi_solid.infrastructure.sqlalchemy.setup.base_repo import AlchemyRepo
from fastapi_solid.infrastructure.sqlalchemy.user.table import UserOrm
from fastapi_solid.utils.converters.alch_to_dc import to_dataclass
from fastapi_solid.utils.converters.json_to_dc import (
    dataclass_from_json,
    dataclass_to_json,
)
from fastapi_solid.utils.logging.logger import get_logger

logger = get_logger(__name__)


class AlchemyUserRepo(UserRepository, AlchemyRepo[UserOrm]):
    model = UserOrm
    user_cache_key = "random_user"
    user_cache_ttl = 60 * 5

    def __init__(self, session: AsyncSession, cache: KeyValueCache):
        super().__init__(session)
        self.cache = cache

    async def get_all(self, pagination: Pagination | None = None) -> list[User]:
        users_orm = await self._get_all(pagination)
        return [to_dataclass(u, User) for u in users_orm]

    async def get_by_id(self, id: UUID) -> User | None:
        user_orm = await self._get_by_id(id)
        return to_dataclass(user_orm, User) if user_orm else None

    async def create(self, user_in: UserIn) -> User:
        created_user = await self._create(user_in.model_dump())
        return to_dataclass(created_user, User)

    async def update(self, id: UUID, update_data: UserUpdate) -> User:
        updated_user = await self._update_by_id(id, update_data.model_dump())
        return to_dataclass(updated_user, User)

    async def delete(self, id: UUID) -> None:
        await self._delete(id)

    # just a showcase how we should cache inside infra level
    async def get_random_user(self) -> User | None:
        if cache := await self._get_cached_user():
            return cache
        users = await self.get_all()
        if not users:
            raise NotFound("No users in database")
        random_user = random.choice(users)
        await self._set_cached_user(random_user)
        return random_user

    async def _get_cached_user(self) -> User | None:
        cache = await self.cache.get(self.user_cache_key)
        if not cache:
            return None
        try:
            return dataclass_from_json(User, cache)
        except Exception:  # damaged cache / old scheme
            logger.debug(
                "Failed to validate cache for key=%s",
                self.user_cache_key,
                exc_info=True,
            )
            await self._drop_cached_user()

    async def _set_cached_user(self, user: User) -> None:
        try:
            json_payload = dataclass_to_json(user)
            await self.cache.set(
                key=self.user_cache_key, value=json_payload, ttl=self.user_cache_ttl
            )
        except Exception:
            logger.exception("Failed to set cache for key=%s", self.user_cache_key)

    async def _drop_cached_user(self) -> None:
        try:
            await self.cache.delete(self.user_cache_key)
        except Exception:
            logger.exception("Failed to delete cache key=%s", self.user_cache_key)
