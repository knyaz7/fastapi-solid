from dependency_injector import containers, providers
from redis.asyncio import Redis  # type: ignore[reportMissingTypeStubs]

from fastapi_solid.application.players.service import PlayerService
from fastapi_solid.application.users.service import UserService
from fastapi_solid.infrastructure.beanie.player.repo import BeaniePlayerRepo
from fastapi_solid.infrastructure.beanie.setup.client import (
    client,  # type: ignore[reportUnknownVariableType]
)
from fastapi_solid.infrastructure.beanie.uow import (
    BeanieUnitOfWork,
    DummyBeanieUnitOfWork,
)
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

    al_session = providers.ContextLocalSingleton(async_session_factory)
    be_session = providers.ContextLocalSingleton(client.start_session)

    alchemy_uow = providers.Factory(AlchemyUnitOfWork, session=al_session)
    beanie_uow = providers.Factory(
        BeanieUnitOfWork if settings.mongo_use_transactions else DummyBeanieUnitOfWork,
        session=be_session,
    )

    users_repo = providers.Factory(
        AlchemyUserRepo, session=al_session, cache=key_value_cache
    )
    users_service = providers.Factory(
        UserService, uow=alchemy_uow, users_repo=users_repo
    )

    player_repo = providers.Factory(BeaniePlayerRepo, session=be_session)
    player_service = providers.Factory(
        PlayerService, uow=beanie_uow, players_repo=player_repo
    )
