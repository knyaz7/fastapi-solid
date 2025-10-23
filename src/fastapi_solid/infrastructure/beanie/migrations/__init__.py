import subprocess
import sys

from fastapi_solid.utils.config.settings import get_settings
from fastapi_solid.utils.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


# fmt: off
def all_forward():
    logger.info("Running all forward migrations")
    subprocess.run([
        "beanie", "migrate",
        "-uri", settings.mongo_dsn,
        "-db", settings.mongo_db_name,
        "-p", settings.mongo_migrations_path
    ])


def one_forward():
    logger.info("Running one forward migration")
    subprocess.run([
        "beanie", "migrate",
        "-uri", settings.mongo_dsn,
        "-db", settings.mongo_db_name,
        "-p", settings.mongo_migrations_path,
        "--distance", "1"
    ])


def one_backward():
    logger.info("Running one backward migration")
    subprocess.run([
        "beanie", "migrate",
        "-uri", settings.mongo_dsn,
        "-db", settings.mongo_db_name,
        "-p", settings.mongo_migrations_path,
        "--distance", "1",
        "--backward"
    ])


def all_backward():
    logger.info("Running all backward migrations")
    subprocess.run([
        "beanie", "migrate",
        "-uri", settings.mongo_dsn,
        "-db", settings.mongo_db_name,
        "-p", settings.mongo_migrations_path,
        "--backward"
    ])


def create_migration():
    if len(sys.argv) < 2:
        logger.error("Migration name is required. "
        "Usage: uv run mongo-migrate-create <migration_name>")
        sys.exit(1)
    
    migration_name = sys.argv[1]
    logger.info(f"Creating migration: {migration_name}")
    
    subprocess.run([
        "beanie", "migrate", 
        "-uri", settings.mongo_dsn,
        "-db", settings.mongo_db_name,
        "-p", settings.mongo_migrations_path,
        "--name", migration_name
    ])
# fmt: on
