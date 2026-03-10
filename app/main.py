"""
main.py

This module initializes the FastAPI application, sets up the database,
registers middleware, and includes API routes.

Features:
- Initializes the database tables from SQLAlchemy models.
- Configures the RequestLoggingMiddleware for logging all incoming HTTP requests.
- Includes the versioned API router under the '/api/v1' prefix.
"""

from app.api.v1.router import api_router
from core.database import Base, engine
from app.middleware.request_middleware import RequestLoggingMiddleware
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI(title="File Upload API")

app.add_middleware(RequestLoggingMiddleware)

app.include_router(api_router, prefix="/api/v1")
