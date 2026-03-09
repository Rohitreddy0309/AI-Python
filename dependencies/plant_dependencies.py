"""
Plant service dependency provider.

This module defines dependency functions used to provide
PlantService instances with an active database session.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from services.plant_services import PlantService


def get_plant_service(db: Session = Depends(get_db)) -> PlantService:
    """
    Provide a PlantService instance with a database session.

    Args:
        db (Session): Database session dependency.

    Returns:
        PlantService: Service instance used for plant operations.
    """
    return PlantService(db)
