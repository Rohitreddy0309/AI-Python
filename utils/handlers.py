from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from utils.exceptions import UserNotFoundException, DuplicateEmailException


def register_exception_handlers(app):

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(request: Request, exc: UserNotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "message": "User not found"
            }
        )

    @app.exception_handler(DuplicateEmailException)
    async def duplicate_email_handler(request: Request, exc: DuplicateEmailException):
        return JSONResponse(
            status_code=409,
            content={
            
                "message": "Email already exists"
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "message": "Validation Error",
                "errors": exc.errors()
            }
        )