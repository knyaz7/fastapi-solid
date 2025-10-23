from types import TracebackType

from pymongo.asynchronous.client_session import AsyncClientSession

from fastapi_solid.application.interfaces.common.uow import UnitOfWork
from fastapi_solid.utils.config.settings import get_settings

settings = get_settings()


class BeanieUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncClientSession):
        self._session = session

    async def __aenter__(self) -> "UnitOfWork":
        await self._session.__aenter__()
        await self._session.start_transaction()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            await self._session.abort_transaction()
        await self._session.__aexit__(exc_type, exc, tb)

    async def commit(self) -> None:
        await self._session.commit_transaction()

    async def rollback(self) -> None:
        await self._session.abort_transaction()


class DummyBeanieUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncClientSession):
        pass

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
