from __future__ import annotations

from uuid import UUID

from fastapi_solid.application.exceptions.error_types import ErrorType


class AppError(Exception):
    def __init__(self, error_type: ErrorType, message: str):
        self.error_type = error_type
        self.message = message

    def __str__(self):
        return self.message


class NotFound(AppError):
    def __init__(self, message: str):
        super().__init__(ErrorType.NOT_FOUND, message)

    @classmethod
    def domain_entity(cls, ent_obj: type, id: UUID | str) -> NotFound:
        message = f"{ent_obj.__name__} with id '{id}' was not found"
        return cls(message)


class ValidationError(AppError):
    def __init__(self, message: str):
        super().__init__(ErrorType.VALIDATION_ERROR, message)
