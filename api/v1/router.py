"""
API Router configuration.

This module registers all version 1 API routes
and aggregates them into a single router.
"""

from fastapi import APIRouter
from api.v1.routes import product

api_router = APIRouter()

api_router.include_router(product.router)
