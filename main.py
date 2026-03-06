from fastapi import FastAPI
from api.v1.router import api_router
from core.database import Base, engine
from models.request_log import RequestLog
from models.student import Student 
from middleware.request_middleware import RequestMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from core.exceptions.base import BaseAppException
from core.exceptions.handlers import (
    base_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    internal_exception_handler
)


# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI instance (must be global)
app = FastAPI(title="Student CRUD API")
app.add_middleware(RequestMiddleware)
app.add_exception_handler(BaseAppException, base_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, internal_exception_handler)

@app.get("/")
def root():
    return {"message": "Student CRUD API is running "}
# Include API routes
app.include_router(api_router, prefix="/api/v1")




#testing
from core.exceptions.custom_exceptions import ForbiddenException

@app.get("/test-error")
def test_error():
    raise ForbiddenException()


from core.exceptions.custom_exceptions import UnauthorizedException
@app.get("/test-auth")
def test_auth():
    raise UnauthorizedException()


