from functools import cache

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

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@cache
def get_settings() -> _Settings:
    return _Settings()  # type: ignore
