from enum import StrEnum


class ErrorType(StrEnum):
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    PERMISSION_DENIED = "permission_denied"
    RATE_LIMITED = "rate_limited"
    PRECONDITION_FAILED = "precondition_failed"
    INVARIANT_VIOLATION = "invariant_violation"
    EXTERNAL_DEPENDENCY_ERROR = "external_dependency_error"
    UNKNOWN = "unknown"
