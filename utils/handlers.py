"""
Global exception handler registration for the FastAPI application.

This module defines custom exception handlers that standardize
error responses across the application. It handles validation
errors and custom application exceptions derived from BaseAppException.
"""

import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from utils.baseExceptions import BaseAppException
from utils.exceptions import DuplicateEmailException, UserNotFoundException

logger = logging.getLogger(__name__)


def register_exception_handlers(app):
    """
    Register all custom exception handlers to the FastAPI app.

    Args:
        app: FastAPI application instance where handlers are registered.
    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """
        Handle request validation errors raised by FastAPI.

        Args:
            request (Request): Incoming request object.
            exc (RequestValidationError): Validation exception raised by FastAPI.

        Returns:
            JSONResponse: Standardized validation error response.
        """
        return JSONResponse(
            status_code=422,
            content={"message": "Validation Error", "errors": exc.errors()},
        )

    @app.exception_handler(BaseAppException)
    async def base_exception_handler(request: Request, exc: BaseAppException):
        """
        Handle custom application exceptions derived from BaseAppException.

        Args:
            request (Request): Incoming request object.
            exc (BaseAppException): Custom application exception.

        Returns:
            JSONResponse: Standardized error response with message and status code.
        """

        logger.error(f"Error: {exc.message}")

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
