from fastapi import HTTPException, status


class BaseAppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        
class UnauthorizedException(BaseAppException):
    def __init__(self, message="Unauthorized access"):
        super().__init__(message, 401)
        
class NotFoundException(BaseAppException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)
                
class ForbiddenException(BaseAppException):
    def __init__(self, message="Access forbidden"):
        super().__init__(message, 403)
        
class WorkflowTransitionException(BaseAppException):
    def __init__(self, message="Invalid workflow transition"):
        super().__init__(message, 400)
        
class RateLimitExceeded(BaseAppException):
    def __init__(self, message="Rate limit exceeded"):
        super().__init__(message, 429)
                                        