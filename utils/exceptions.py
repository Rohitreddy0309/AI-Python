"""Custom exception types and FastAPI exception handlers."""

from fastapi import Request
from fastapi.responses import JSONResponse

from core.config import logger


class BaseAppException(Exception):
    """Base exception type for application-specific errors."""

    def __init__(self, name: str, detail: str, status_code: int = 400):
        self.name = name
        self.detail = detail
        self.status_code = status_code


class NotFoundException(BaseAppException):
    """Raised when an entity cannot be found."""

    def __init__(self, entity_name: str = "Not Found", entity_id: int | str = " none"):
        super().__init__(
            name=f"{entity_name}NotFound",
            detail=f"{entity_name} not found with ID '{entity_id}' not found",
            status_code=404,
        )


class DuplicateEntryException(BaseAppException):
    """Raised when attempting to create a duplicate resource."""

    def __init__(
        self,
        entity_name: str = "Duplicate Entry",
        field_name: str = "field",
        field_value: str | int = "",
    ):
        super().__init__(
            name=f"{entity_name}DuplicateEntry",
            detail=f"{entity_name} with {field_name} '{field_value}' already exists",
            status_code=400,
        )


class DatabaseException(BaseAppException):
    """Raised when a database error occurs."""

    def __init__(self, detail: str = "Database error occurred"):
        super().__init__(name="DatabaseException", detail=detail, status_code=500)


class UnauthorizedException(BaseAppException):
    """Raised when requester is not authorized."""

    def __init__(self, detail="Unauthorized access"):
        super().__init__(name="UnauthorizedException", detail=detail, status_code=401)


class ForbiddenException(BaseAppException):
    """Raised when requester does not have required permissions."""

    def __init__(self, detail="Access forbidden"):
        super().__init__(name="ForbiddenException", detail=detail, status_code=403)


class WorkflowTransitionException(BaseAppException):
    """Raised when an invalid workflow transition is attempted."""

    def __init__(self, detail="Invalid workflow transition"):
        super().__init__(
            name="WorkflowTransitionException", detail=detail, status_code=400
        )


class RateLimitExceeded(BaseAppException):
    """Raised when a user exceeds the configured rate limit."""

    def __init__(self, detail="Rate limit exceeded"):
        super().__init__(name="RateLimitExceeded", detail=detail, status_code=429)


async def app_exception_handler(request: Request, exc: BaseAppException):
    """Convert application-specific exceptions into JSON responses."""

    logger.error(
        "BaseAppException occurred: %s - %s | path=%s",
        exc.name,
        exc.detail,
        request.url.path,
    )
    return JSONResponse(
        status_code=exc.status_code, content={"error": exc.name, "detail": exc.detail}
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Fallback handler for unexpected exceptions."""

    logger.error("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "detail": str(exc),
            "path": str(request.url.path),
        },
    )
