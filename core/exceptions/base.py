"""
Base exception module.

Defines the base application exception used by all custom exceptions.
"""


class BaseAppException(Exception):
    """Base exception class for all application-specific errors."""

    def __init__(self, message: str, status_code: int):
        """Initialize exception with message and HTTP status code."""
        self.message = message
        self.status_code = status_code
