from abc import ABC, abstractmethod
from uuid import UUID

from fastapi_solid.application.interfaces.common.pagination import Pagination
from fastapi_solid.application.users.dto import UserIn, UserUpdate
from fastapi_solid.domain.user.model import User


class UserRepository(ABC):
    @abstractmethod
    async def get_all(self, pagination: Pagination | None = None) -> list[User]: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> User | None: ...

    @abstractmethod
    async def get_random_user(self) -> User | None: ...

    @abstractmethod
    async def create(self, user_in: UserIn) -> User: ...

    @abstractmethod
    async def update(self, id: UUID, update_data: UserUpdate) -> User: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
