import uvicorn

from fastapi_solid.infrastructure.fastapi.create_app import create_app
from fastapi_solid.utils.config.settings import get_settings
from fastapi_solid.utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

app = create_app()


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port, use_colors=True)


if __name__ == "__main__":
    main()
