from dependency_injector import containers, providers
from redis.asyncio import Redis  # type: ignore[reportMissingTypeStubs]

from fastapi_solid.application.users.service import UserService
from fastapi_solid.infrastructure.redis.cache import RedisCache
from fastapi_solid.infrastructure.sqlalchemy.setup.engine import async_session_factory
from fastapi_solid.infrastructure.sqlalchemy.uow import AlchemyUnitOfWork
from fastapi_solid.infrastructure.sqlalchemy.user.repo import AlchemyUserRepo
from fastapi_solid.utils.config.settings import get_settings

settings = get_settings()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["fastapi_solid.infrastructure.fastapi.endpoints.v1"]
    )  # fastapi integration

    redis = providers.Singleton(
        Redis.from_url,  # type: ignore[reportUnknownMemberType]
        settings.redis_dsn,
    )

    key_value_cache = providers.Singleton(RedisCache, redis_client=redis)

    session = providers.ContextLocalSingleton(async_session_factory)

    unit_of_work = providers.Factory(AlchemyUnitOfWork, session=session)

    users_repo = providers.Factory(
        AlchemyUserRepo, session=session, cache=key_value_cache
    )

    users_service = providers.Factory(
        UserService, uow=unit_of_work, users_repo=users_repo
    )
