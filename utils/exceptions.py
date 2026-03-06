from core.exceptions.base import BaseAppException
from fastapi import status


class ConflictException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            
        )


class NotFoundException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            
        )