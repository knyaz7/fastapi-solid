import logging

from rich.console import Console
from rich.logging import RichHandler

from fastapi_solid.utils.config.settings import get_settings

from .lib_log_filter import LibraryLogFilter

settings = get_settings()


def setup_logging():
    # force_terminal=True for colored terminal output
    rich_console = Console(style="bold cyan", width=200, force_terminal=True)
    rich_handler = RichHandler(
        console=rich_console,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        tracebacks_word_wrap=False,
        log_time_format="[%d/%m/%y %H:%M:%S]",
    )
    rich_handler.addFilter(LibraryLogFilter())
    rich_handler.setFormatter(logging.Formatter("[ %(funcName)s() ] - %(message)s"))

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.logging_level)
    root_logger.addHandler(rich_handler)


def get_logger(name: str):
    return logging.getLogger(settings.logging_app_prefix + "." + name)
