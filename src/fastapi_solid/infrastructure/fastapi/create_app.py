from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from fastapi_solid.infrastructure.beanie import docs
from fastapi_solid.infrastructure.beanie.setup.client import (
    client,  # type: ignore[reportUnknownVariableType]
    init_beanie_async,
)
from fastapi_solid.infrastructure.di.container import Container

from .endpoints import api_v1_router
from .error_handler import register_error_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()

    redis = container.redis()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    app.container = container  # type: ignore[reportAttributeAccessIssue]

    await init_beanie_async(docs)
    yield
    await client.close()
    await redis.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, docs_url="/api/docs")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_v1_router)
    register_error_handlers(app)
    return app
