"""
Dependency providers for product-related services.

This module defines FastAPI dependency functions used to
inject service layer objects into route handlers.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from services.product_service import ProductService


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """
    Dependency that provides a ProductService instance.

    It injects the database session into the service layer,
    allowing route handlers to access business logic without
    directly interacting with the database.
    """
    return ProductService(db)
