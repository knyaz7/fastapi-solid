from logging import Filter, LogRecord, getLevelNamesMapping

from fastapi_solid.utils.config.settings import get_settings

settings = get_settings()


class LibraryLogFilter(Filter):
    def __init__(self):
        level_mapping = getLevelNamesMapping()
        self.logging_lib_level = level_mapping[settings.logging_lib_level]

    def filter(self, record: LogRecord) -> bool:
        if record.name.startswith(settings.logging_app_prefix):
            return True
        return record.levelno >= self.logging_lib_level
