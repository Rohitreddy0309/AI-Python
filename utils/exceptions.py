from fastapi.responses import JSONResponse
from fastapi import Request
from core.config import logger

class AppException(Exception):
    def __init__(self, name: str, detail: str, status_code: int = 400):
        self.name = name
        self.detail = detail
        self.status_code = status_code
     
class NotFoundException(AppException):
    def __init__(self, entity_name: str = "Not Found", entity_id: int | str = " none"):
        super().__init__(
            name = f"{entity_name}NotFound",
            detail = f"{entity_name} not found with ID '{entity_id}' not found",
            status_code=404
            )
class DuplicateEntryException(AppException):
    def __init__(self, entity_name: str = "Duplicate Entry", field_name: str = "field", field_value: str | int = ""):
        super().__init__(
            name = f"{entity_name}DuplicateEntry",
            detail = f"{entity_name} with {field_name} '{field_value}' already exists",
            status_code=400
        )

class DatabaseException(AppException):
    def __init__(self, detail: str = "Database error occurred"):
        super().__init__(
            name = "DatabaseException",
            detail = detail,
            status_code=500
        )

async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"AppException occurred: {exc.name} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.name, "detail": exc.detail}
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "detail": str(exc),
            "path": str(request.url.path)
            }
    )