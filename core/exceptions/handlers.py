"""
Global exception handlers for the application.

These handlers convert different exceptions into
standardized JSON error responses.
"""

import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from core.exceptions.base import BaseAppException

logger = logging.getLogger(__name__)


def build_error_response(request: Request, message: str, status_code: int):
    """Build a standardized JSON error response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "error": True,
            "message": message,
            "status_code": status_code,
            "path": request.url.path,
        },
    )


async def base_exception_handler(request: Request, exc: BaseAppException):
    """Handle custom application exceptions."""
    logger.error("Error: %s", exc.message)
    return build_error_response(request, exc.message, exc.status_code)


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions."""
    logger.error("HTTP Error: %s", exc.detail)
    return build_error_response(request, exc.detail, exc.status_code)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.error("Validation Error: %s", exc)
    return build_error_response(request, "Validation Error", 422)


async def internal_exception_handler(request: Request, exc: Exception):
    """Handle unexpected internal server errors."""
    logger.error("Unhandled Error: %s",exc)
    return build_error_response(request, "Internal Server Error", 500)
