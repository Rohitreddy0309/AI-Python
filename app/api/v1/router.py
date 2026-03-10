"""
API Router Configuration.

This module creates the main API router and includes
all version 1 routes such as file and student routes.
It acts as a central place to register all API endpoints.
"""

from app.api.v1.routes import file, student
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(file.router, prefix="/files", tags=["Files"])
api_router.include_router(student.router)
