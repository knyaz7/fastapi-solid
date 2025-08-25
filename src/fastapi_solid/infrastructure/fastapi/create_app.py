from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from fastapi_solid.infrastructure.di.container import Container

from .endpoints import api_v1_router
from .error_handler import register_error_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()

    redis = container.redis()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    app.container = container  # type: ignore[reportAttributeAccessIssue]
    yield
    await redis.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, docs_url="/api/docs")
    app.include_router(api_v1_router)
    register_error_handlers(app)
    return app
