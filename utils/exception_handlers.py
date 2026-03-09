"""
Global exception handlers for the application.

This module defines custom handlers for application-level exceptions.
These handlers ensure that all errors return a consistent JSON response
structure and are properly logged for debugging and monitoring.
"""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from utils.exceptions import BaseAppException

logger = logging.getLogger(__name__)


async def base_exception_handler(request: Request, exc: BaseAppException):
    """
    Handle all custom application exceptions.

    Logs the error details and returns a structured JSON response
    containing the error type, message, and status code.

    Args:
        request (Request): Incoming HTTP request.
        exc (BaseAppException): Raised application exception.

    Returns:
        JSONResponse: Structured error response.
    """

    logger.error(
        "Error occurred | Path: %s | Status: %s | Message: %s",
        request.url.path,
        exc.status_code,
        exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message,
                "status_code": exc.status_code,
            },
        },
    )
