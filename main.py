"""
Main entry pointfor the FastAPI Product CRUD application.

This file initializes the FastAPI app, registers middleware,
loads database models, and includes API routers.
"""

from fastapi import FastAPI

from api.v1.router import api_router
from core.database import Base, engine
from middleware.request_logger import RequestLoggingMiddleware

app = FastAPI()


Base.metadata.create_all(bind=engine)


app.add_middleware(RequestLoggingMiddleware)


app.include_router(api_router)


@app.get("/")
def root():
    """
    Root endpoint to verify that the API service is running.
    """
    return {"message": "CRUD API is running "}
