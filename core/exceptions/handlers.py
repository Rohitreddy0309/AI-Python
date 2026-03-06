import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .base import BaseAppException

logger = logging.getLogger(__name__)


def build_error_response(request: Request, message: str, status_code: int):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": True,
            "message": message,
            "status_code": status_code,
            "path": request.url.path
        }
    )


async def base_exception_handler(request: Request, exc: BaseAppException):

    logger.error(f"Error: {exc.message}")

    return build_error_response(request, exc.message, exc.status_code)


async def http_exception_handler(request: Request, exc: HTTPException):

    logger.error(f"HTTP Error: {exc.detail}")

    return build_error_response(request, exc.detail, exc.status_code)


async def validation_exception_handler(request: Request, exc: RequestValidationError):

    logger.error(f"Validation Error: {exc}")

    return build_error_response(request, "Validation Error", 422)


async def internal_exception_handler(request: Request, exc: Exception):

    logger.error(f"Unhandled Error: {exc}")

    return build_error_response(request, "Internal Server Error", 500)