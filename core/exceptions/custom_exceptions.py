from .base import BaseAppException

class UnauthorizedException(BaseAppException):
    def __init__(self,message="Unauthorized Acess"):
        super().__init__(message, 401)


class ForbiddenException(BaseAppException):
    def __init__(self,message="Forbidden Acess"):
        super().__init__(message, 403)


class WorkFlowTransitionException(BaseAppException):
    def __init__(self,message="Invalid Workflow Transition"):
        super().__init__(message, 409)


class RateLimitException(BaseAppException):
    def __init__(self,message="Rate limit Exceeded"):
        super().__init__(message,429)