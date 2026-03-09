"""
Custom application exceptions.

This module defines custom exception classes used across the
application to provide consistent error handling and structured
API error responses.
"""

from fastapi import HTTPException


class BaseAppException(HTTPException):
    """
    Base exception class for all application-level exceptions.

    Extends FastAPI's HTTPException and adds a custom message
    attribute for structured error responses.
    """

    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)
        self.message = message


class NotFoundException(BaseAppException):
    """
    Exception raised when a requested resource cannot be found.
    """

    def __init__(self, message: str = "Resource not found"):
        super().__init__(404, message)


class UnauthorizedException(BaseAppException):
    """
    Exception raised when authentication is required but missing.
    """

    def __init__(self, message: str = "Authentication required"):
        super().__init__(401, message)


class ForbiddenException(BaseAppException):
    """
    Exception raised when a user does not have permission
    to perform a specific action.
    """

    def __init__(self, message: str = "Access to this resource is forbidden"):
        super().__init__(403, message)


class WorkflowTransitionException(BaseAppException):
    """
    Exception raised when an invalid workflow state transition occurs.
    """

    def __init__(self, message: str = "Invalid workflow transition"):
        super().__init__(400, message)


class RateLimitExceeded(BaseAppException):
    """
    Exception raised when a user exceeds the allowed request rate.
    """

    def __init__(self, message: str = "Too many requests. Please try again later"):
        super().__init__(429, message)
