class BaseAppException(Exception):
    """
    Base exception class for application-specific errors.

    This class extends the built-in Exception and allows attaching
    a custom error message along with an HTTP status code. Other
    custom exceptions in the application can inherit from this class.
    """

    def __init__(self, message: str, status_code: int):
        """
        Initialize the BaseAppException.

        Args:
            message (str): Description of the error.
            status_code (int): HTTP status code associated with the error.
        """
        self.message = message
        self.status_code = status_code
