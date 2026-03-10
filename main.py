"""Main entrypoint for the Employee & Task Management API.

This module creates the FastAPI application, registers routers,
initializes the database, and configures middleware + exception
handlers.
"""

import uvicorn
from fastapi import FastAPI

from api import emp_routes, task_routes
from core.db import Base, engine
from middleware.request_middleware import RequestLoggingMiddleware
from utils.exceptions import (BaseAppException, app_exception_handler,
                              generic_exception_handler)

app = FastAPI(title="Employee & Task Management API")

# Ensure the database tables are created before serving requests.
Base.metadata.create_all(bind=engine)

# Include API routers (employee and task endpoints).
app.include_router(emp_routes.router)
app.include_router(task_routes.router)

# Register global exception handlers for both application-specific
# and generic exceptions.
app.add_exception_handler(BaseAppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Add middleware for request logging / request lifecycle concerns.
app.add_middleware(RequestLoggingMiddleware)


@app.get("/", tags=["Health"])
def root():
    """A simple healthcheck / welcome endpoint."""

    return {"message": "Welcome to the Employee & Task Management API"}


if __name__ == "__main__":
    # Start the app using Uvicorn when run as a script.
    uvicorn.run(app, host="127.0.0.1", port=8000)
