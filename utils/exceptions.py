"""
Custom application-specific exception classes.

These exceptions extend BaseAppException and represent different
error scenarios in the application with predefined HTTP status codes.
"""

from utils.baseExceptions import BaseAppException


class UserNotFoundException(BaseAppException):
    """
    Exception raised when a requested user is not found in the system.
    """

    def __init__(self, message="User not found"):
        """
        Initialize the UserNotFoundException.

        Args:
            message (str): Error message describing the issue.
        """
        super().__init__(message, 404)


class DuplicateEmailException(BaseAppException):
    """
    Exception raised when attempting to create a user with
    an email that already exists.
    """

    def __init__(self, message="Email already exists"):
        """
        Initialize the DuplicateEmailException.

        Args:
            message (str): Error message describing the issue.
        """
        super().__init__(message, 409)


class UnauthorizedException(BaseAppException):
    """
    Exception raised when a user tries to access a resource
    without proper authentication.
    """

    def __init__(self, message="Unauthorized access"):
        """
        Initialize the UnauthorizedException.

        Args:
            message (str): Error message describing the issue.
        """
        super().__init__(message, 401)


class ForbiddenException(BaseAppException):
    """
    Exception raised when a user does not have permission
    to access a specific resource.
    """

    def __init__(self, message="Access forbidden"):
        """
        Initialize the ForbiddenException.

        Args:
            message (str): Error message describing the issue.
        """
        super().__init__(message, 403)


class WorkflowTransitionException(BaseAppException):
    """
    Exception raised when an invalid workflow transition occurs.
    """

    def __init__(self, message="Invalid workflow transition"):
        """
        Initialize the WorkflowTransitionException.

        Args:
            message (str): Error message describing the issue.
        """
        super().__init__(message, 400)


class RateLimitExceeded(BaseAppException):
    """
    Exception raised when a user exceeds the allowed number of requests.
    """

    def __init__(self, message="Rate limit exceeded"):
        """
        Initialize the RateLimitExceeded exception.

        Args:
            message (str): Error message describing the issue.
        """
        super().__init__(message, 429)
