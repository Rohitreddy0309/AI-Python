from fastapi import HTTPException

class BaseAppException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)
        self.message = message


class NotFoundException(BaseAppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(404, message)


class UnauthorizedException(BaseAppException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(401, message)


class ForbiddenException(BaseAppException):
    def __init__(self, message: str = "Invalid workflow transition"):
        super().__init__(403, message)


class WorkflowTransitionException(BaseAppException):
    def __int__(self, message: str = "Invalid workflow transition"):
        super().__init__(400, message)


class RateLimitExceeded(BaseAppException):
    def __init__(self, message: str = "Too many requests. Please try again later"):
        super().__init__(429, message)
        

