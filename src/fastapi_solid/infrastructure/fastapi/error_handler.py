from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from fastapi_solid.application.exceptions.app_error import AppError
from fastapi_solid.application.exceptions.error_types import ErrorType

HTTP_MAP = {
    ErrorType.NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorType.CONFLICT: status.HTTP_409_CONFLICT,
    ErrorType.VALIDATION_ERROR: status.HTTP_422_UNPROCESSABLE_ENTITY,
    ErrorType.PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
    ErrorType.RATE_LIMITED: status.HTTP_429_TOO_MANY_REQUESTS,
    ErrorType.PRECONDITION_FAILED: status.HTTP_412_PRECONDITION_FAILED,
    ErrorType.INVARIANT_VIOLATION: status.HTTP_422_UNPROCESSABLE_ENTITY,
    ErrorType.EXTERNAL_DEPENDENCY_ERROR: status.HTTP_502_BAD_GATEWAY,
    ErrorType.UNKNOWN: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _(request: Request, exc: AppError):
        status_code = HTTP_MAP.get(exc.error_type, 500)
        return JSONResponse(status_code=status_code, content=str(exc))
