import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from utils.baseExceptions import BaseAppException
from utils.exceptions import DuplicateEmailException, UserNotFoundException

logger = logging.getLogger(__name__)


def register_exception_handlers(app):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=422,
            content={"message": "Validation Error", "errors": exc.errors()},
        )

    @app.exception_handler(BaseAppException)
    async def base_exception_handler(request: Request, exc: BaseAppException):

        logger.error(f"Error: {exc.message}")

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "type": exc.__class__.__name__,
                    "message": exc.message,
                    "status_code": exc.status_code,
                },
            },
        )
