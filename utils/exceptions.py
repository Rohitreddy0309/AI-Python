from utils.baseExceptions import BaseAppException


class UserNotFoundException(BaseAppException):

    def __init__(self, message="User not found"):
        super().__init__(message, 404)


class DuplicateEmailException(BaseAppException):

    def __init__(self, message="Email already exists"):
        super().__init__(message, 409)


class UnauthorizedException(BaseAppException):

    def __init__(self, message="Unauthorized access"):
        super().__init__(message, 401)


class ForbiddenException(BaseAppException):

    def __init__(self, message="Access forbidden"):
        super().__init__(message, 403)


class WorkflowTransitionException(BaseAppException):

    def __init__(self, message="Invalid workflow transition"):
        super().__init__(message, 400)


class RateLimitExceeded(BaseAppException):

    def __init__(self, message="Rate limit exceeded"):
        super().__init__(message, 429)
