"""
Custom application exceptions.

This module defines application-specific exception classes used
throughout the API to standardize error handling and responses.
"""


class BaseAppException(Exception):
    """Base exception class for all custom application errors."""

    def __init__(self, message: str, status_code: int = 400):
        """
        Initialize the base application exception.

        Args:
            message (str): Error message describing the issue.
            status_code (int): HTTP status code associated with the error.
        """
        self.message = message
        self.status_code = status_code


class UnauthorizedException(BaseAppException):
    """Exception raised when a user is not authorized to access a resource."""

    def __init__(self, message="Unauthorized access"):
        super().__init__(message, 401)


class NotFoundException(BaseAppException):
    """Exception raised when a requested resource cannot be found."""

    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)


class ForbiddenException(BaseAppException):
    """Exception raised when access to a resource is forbidden."""

    def __init__(self, message="Access forbidden"):
        super().__init__(message, 403)


class WorkflowTransitionException(BaseAppException):
    """Exception raised when an invalid workflow transition occurs."""

    def __init__(self, message="Invalid workflow transition"):
        super().__init__(message, 400)


class RateLimitExceeded(BaseAppException):
    """Exception raised when the API rate limit is exceeded."""

    def __init__(self, message="Rate limit exceeded"):
        super().__init__(message, 429)
