from collections.abc import Sequence
from typing import Any

from beanie import Document, init_beanie  # type: ignore[reportUnknownVariableType]
from pymongo import AsyncMongoClient

from fastapi_solid.utils.config.settings import get_settings

settings = get_settings()

client = AsyncMongoClient(  # type: ignore[reportUnknownVariableType]
    settings.mongo_dsn,
    serverSelectionTimeoutMS=3_000,
    connectTimeoutMS=2_000,
    socketTimeoutMS=10_000,
    maxPoolSize=50,
    minPoolSize=1,
    uuidRepresentation="standard",
    retryWrites=True,
)


async def init_beanie_async(docs: Sequence[type[Document]]) -> AsyncMongoClient[Any]:
    mongo_db = client.get_database(settings.mongo_db_name)  # type: ignore[reportUnknownVariableType]
    await init_beanie(mongo_db, document_models=docs)
    return client  # type: ignore[reportUnknownVariableType]
