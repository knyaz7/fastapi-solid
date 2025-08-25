from typing import Any


class Singleton(type):
    _instances: dict[type, object] = {}

    def __call__(cls, *args: Any, **kwargs: Any):
        if cls not in cls._instances:  # type: ignore[reportUnnecessaryContains]
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
