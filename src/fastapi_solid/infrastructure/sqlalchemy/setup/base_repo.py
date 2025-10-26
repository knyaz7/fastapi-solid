from collections.abc import Mapping, Sequence
from typing import Any, overload
from uuid import UUID

from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_solid.application.exceptions.app_error import NotFound
from fastapi_solid.application.interfaces.common.pagination import Pagination
from fastapi_solid.utils.logging.logger import get_logger

from .base_model import Base

logger = get_logger(__name__)


class AlchemyRepo[T: Base]:
    model: type[T]

    def __init__(self, session: AsyncSession):
        self._session = session

    async def _get_all(self, pagination: Pagination | None = None) -> Sequence[T]:
        query = select(self.model)
        if pagination:
            query = query.limit(pagination.limit).offset(pagination.offset)
        res = await self._session.execute(query)
        return res.scalars().all()

    async def _get_by_id(self, id: UUID) -> T | None:
        query = select(self.model).where(self.model.id == id)
        res = await self._session.execute(query)
        return res.scalar_one_or_none()

    async def _count(self) -> int:
        query = select(func.count(self.model.id))
        res = await self._session.execute(query)
        return res.scalar_one()

    @overload
    async def _create(self, values: Mapping[str, Any]) -> T: ...
    @overload
    async def _create(self, values: Sequence[Mapping[str, Any]]) -> Sequence[T]: ...

    async def _create(
        self, values: Mapping[str, Any] | Sequence[Mapping[str, Any]]
    ) -> T | Sequence[T]:
        stmt = insert(self.model).values(values).returning(self.model)
        res = await self._session.execute(stmt)
        if isinstance(values, dict):
            created_entity = res.scalar_one()
            logger.debug(f"Created {created_entity}")
            return created_entity
        created_entities = res.scalars().all()
        logger.debug(
            "Created %s entities of %s",
            len(created_entities),
            self.model.__class__.__name__,
        )
        return created_entities

    async def _update_by_id(self, id: UUID, values: Mapping[str, Any]) -> T:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(values)
            .returning(self.model)
        )
        res = await self._session.execute(stmt)
        updated = res.scalar_one_or_none()
        if updated is None:
            raise NotFound(f"{self.model.__name__[:-3]} with id={id} not found")
        logger.debug(f"Updated {updated}")
        return updated

    async def _delete(self, id: UUID) -> None:
        entity = await self._session.get(self.model, id)
        entity_repr = repr(entity)
        if not entity:
            raise NotFound(f"{self.model.__name__[:-3]} with id={id} not found")
        await self._session.delete(entity)
        logger.debug(f"Deleted {entity_repr}")
