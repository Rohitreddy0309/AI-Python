from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.v1.router import router
from core.database import base, engine
from core.request_logger import RequestLoggerMiddleware
from models.file_data import FileData
from utils.handlers import register_exception_handlers

app = FastAPI()

# Register exception handlers
register_exception_handlers(app)

# Middleware
app.add_middleware(RequestLoggerMiddleware)

# Static file folder
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Create tables
base.metadata.create_all(bind=engine)

# Include routers
app.include_router(router)
