"""
Main entry point for the Student CRUD API application.

This module initializes the FastAPI application, registers middleware,
sets up global exception handlers, and mounts API routers.
"""

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from api.v1.router import api_router
from core.database import Base, engine
from core.exceptions.base import BaseAppException
from core.exceptions.handlers import (
    base_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    internal_exception_handler,
)
from middleware.request_middleware import RequestMiddleware

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="Student CRUD API")

# Register middleware for request logging and tracing
app.add_middleware(RequestMiddleware)

# Register global exception handlers
app.add_exception_handler(BaseAppException, base_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, internal_exception_handler)


@app.get("/")
def root():
    """Root endpoint used as a health check for the API."""

    return {"message": "Student CRUD API is running "}


# Register API routers with versioned prefix
app.include_router(api_router, prefix="/api/v1")
