from functools import cache
from typing import Literal

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    api_port: int = 8000

    logging_level: str
    logging_lib_level: str = "WARNING"
    logging_app_prefix: str = "app"

    db_scheme: str = "postgresql+asyncpg"
    db_host: str
    db_port: int
    db_username: str
    db_password: str
    db_name: str

    redis_dsn: str

    mongo_scheme: Literal["mongodb", "mongodb+srv"] = "mongodb"
    mongo_host: str
    mongo_port: int
    mongo_username: str
    mongo_password: str
    mongo_db_name: str
    mongo_auth_db: str
    mongo_migrations_path: str = "src/fastapi_solid/infrastructure/beanie/migrations/"
    mongo_use_transactions: bool = True

    @property
    def db_dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=self.db_scheme,
                host=self.db_host,
                port=self.db_port,
                username=self.db_username,
                password=self.db_password,
                path=self.db_name,
            )
        )

    @property
    def mongo_dsn(self) -> str:
        return (
            f"{self.mongo_scheme}://{self.mongo_username}:{self.mongo_password}"
            f"@{self.mongo_host}:{self.mongo_port}/"
            f"?replicaSet=rs0&authSource={self.mongo_auth_db}&directConnection=false"
            f"&retryWrites=true&w=majority"
        )

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@cache
def get_settings() -> _Settings:
    return _Settings()  # type: ignore
