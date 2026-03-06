from fastapi import Request
from fastapi.responses import JSONResponse
from utils.exceptions import BaseAppException

async def app_exception_handler(request: Request, exc: BaseAppException):
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "path": request.url.path
        }
    )