from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from services.plant_services import PlantService


def get_plant_service(db: Session = Depends(get_db)) -> PlantService:
    return PlantService(db)