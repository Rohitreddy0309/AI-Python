"""
Custom exception handler.

This module defines a global exception handler for application-specific
exceptions derived from BaseAppException. It formats error responses
in a consistent JSON structure.
"""

from fastapi import Request
from fastapi.responses import JSONResponse

from utils.exceptions import BaseAppException


async def app_exception_handler(request: Request, exc: BaseAppException):
    """
    Handle custom application exceptions.

    Args:
        request (Request): Incoming HTTP request.
        exc (BaseAppException): Raised application exception.

    Returns:
        JSONResponse: Structured error response.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "path": request.url.path,
        },
    )
