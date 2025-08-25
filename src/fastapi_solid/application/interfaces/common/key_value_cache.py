from abc import ABC, abstractmethod

CacheResponse = bytes | None


class KeyValueCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> CacheResponse: ...

    @abstractmethod
    async def set(self, key: str, value: str | bytes, ttl: int) -> None: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...
