from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from fastapi_solid.utils.config.settings import get_settings

settings = get_settings()

async_engine = create_async_engine(settings.db_dsn)
async_session_factory = async_sessionmaker(async_engine)
