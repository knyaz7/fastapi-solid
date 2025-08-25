from redis.asyncio import Redis  # type: ignore[reportMissingTypeStubs]

from fastapi_solid.application.interfaces.common.key_value_cache import (
    CacheResponse,
    KeyValueCache,
)


class RedisCache(KeyValueCache):
    def __init__(self, redis_client: Redis):
        self._redis_client = redis_client

    async def get(self, key: str) -> CacheResponse:
        return await self._redis_client.get(key)  # type: ignore[reportUnknownVariableType]

    async def set(self, key: str, value: str | bytes, ttl: int) -> None:
        await self._redis_client.set(key, value, ex=ttl)  # type: ignore[reportUnknownVariableType]

    async def delete(self, key: str) -> None:
        await self._redis_client.delete(key)  # type: ignore[reportUnknownVariableType]
