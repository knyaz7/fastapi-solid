from collections.abc import Sequence
from typing import Any, overload
from uuid import UUID

from beanie import Document
from pymongo.asynchronous.client_session import AsyncClientSession

from fastapi_solid.application.exceptions.app_error import NotFound
from fastapi_solid.application.interfaces.common.pagination import Pagination
from fastapi_solid.utils.logging.logger import get_logger

logger = get_logger(__name__)


class BeanieRepo[T: Document]:
    model: type[T]

    def __init__(self, session: AsyncClientSession):
        self._session = session

    async def _get_all(self, pagination: Pagination | None = None) -> Sequence[T]:
        cursor = self.model.find_all(session=self._session)
        if pagination:
            cursor = cursor.skip(pagination.offset).limit(pagination.limit)
        return await cursor.to_list()

    async def _get_by_id(self, id: UUID) -> T | None:
        return await self.model.find_one(self.model.id == id, session=self._session)

    async def _count(self) -> int:
        return await self.model.find_all(session=self._session).count()

    @overload
    async def _create(self, values: dict[str, Any]) -> T: ...
    @overload
    async def _create(self, values: Sequence[dict[str, Any]]) -> Sequence[T]: ...

    async def _create(
        self, values: dict[str, Any] | Sequence[dict[str, Any]]
    ) -> T | Sequence[T]:
        if isinstance(values, dict):
            doc = self.model(**values)
            await doc.insert(session=self._session)
            return doc

        if not values:
            return []

        docs = [self.model(**payload) for payload in values]
        await self.model.insert_many(docs, session=self._session)
        return docs

    async def _update_by_id(
        self, id: UUID, values: dict[str, Any], exclude_none: bool = False
    ) -> T:
        if exclude_none:
            values = {k: v for k, v in values.items() if v is not None}

        if values:
            result = await self.model.find_one(
                self.model.id == id, session=self._session
            ).set(values, session=self._session)

            matched = getattr(result, "matched_count", 0)

            if matched == 0:
                raise NotFound(f"{self.model.__name__[:-3]} with id={id} not found")

        updated_doc = await self.model.find_one(
            self.model.id == id, session=self._session
        )
        if not updated_doc:
            raise NotFound(
                f"{self.model.__name__[:-3]} with id={id} not found after update"
            )
        return updated_doc

    async def _delete(self, id: UUID) -> None:
        res = await self.model.find_one(
            self.model.id == id, session=self._session
        ).delete(session=self._session)
        deleted = getattr(res, "deleted_count", 0) if res is not None else 0
        if deleted == 0:
            raise NotFound(f"{self.model.__name__[:-3]} with id={id} not found")
