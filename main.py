from fastapi import FastAPI
from core.database import engine, Base
from api.v1.router import api_router
from fastapi.staticfiles import StaticFiles
from middleware.request_logging_middleware import RequestLoggingMiddleware
from utils.exceptions import BaseAppException
from utils.exception_handler import app_exception_handler

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plant Care API with PostgreSQL")

# Include API router
app.include_router(api_router, prefix="/api/v1")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.add_middleware(RequestLoggingMiddleware)
app.add_exception_handler(BaseAppException, app_exception_handler)
