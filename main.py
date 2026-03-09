"""
Main entry point for the Plant Care API.

This module initializes the FastAPI application, sets up database tables,
registers API routes, configures static file handling, middleware,
and custom exception handling.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.v1.router import api_router
from core.database import Base, engine
from middleware.request_logging_middleware import RequestLoggingMiddleware
from utils.exception_handler import app_exception_handler
from utils.exceptions import BaseAppException

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plant Care API with PostgreSQL")

app.include_router(api_router, prefix="/api/v1")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(RequestLoggingMiddleware)

app.add_exception_handler(BaseAppException, app_exception_handler)
