from fastapi import Request
from fastapi.responses import JSONResponse
import logging

from utils.exceptions import BaseAppException

logger = logging.getLogger(__name__)

async def base_exception_handler(request: Request, exc: BaseAppException):

    logger.error(
        f"Error occured | Path: {request.url.path} | "
        f"Status: {exc.status_code} | Message: {exc.message}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message,
                "status_code": exc.status_code
            }

        }
    )

