"""
Custom exception classes for the application.

Each exception inherits from BaseAppException and
represents a specific HTTP error.
"""

from core.exceptions.base import BaseAppException


class UnauthorizedException(BaseAppException):
    """Raised when a user is not authenticated."""

    def __init__(self, message="Unauthorized Access"):
        super().__init__(message, 401)


class ForbiddenException(BaseAppException):
    """Raised when a user does not have permission to access a resource."""

    def __init__(self, message="Forbidden Access"):
        super().__init__(message, 403)


class WorkFlowTransitionException(BaseAppException):
    """Raised when an invalid workflow transition occurs."""

    def __init__(self, message="Invalid Workflow Transition"):
        super().__init__(message, 409)


class RateLimitException(BaseAppException):
    """Raised when a user exceeds the allowed rate limit."""

    def __init__(self, message="Rate limit exceeded"):
        super().__init__(message, 429)


class ConflictException(BaseAppException):
    """Raised when a conflict occurs (e.g., duplicate resource)."""

    def __init__(self, message="Conflict occurred"):
        super().__init__(message, 409)


class NotFoundException(BaseAppException):
    """Raised when a requested resource cannot be found."""

    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)
