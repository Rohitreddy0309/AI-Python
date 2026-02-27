from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from services.plant_services import PlantService
from schemas.schemas import PlantCreate, PlantResponse

router = APIRouter()
service = PlantService()


@router.post("/", response_model=PlantResponse)
def create_plant(plant: PlantCreate, db: Session = Depends(get_db)):
    return service.create_plant(db, plant)


@router.get("/", response_model=list[PlantResponse])
def get_plants(db: Session = Depends(get_db)):
    return service.get_plants(db)


@router.get("/{plant_id}", response_model=PlantResponse)
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    try:
        return service.get_plant(db, plant_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Plant not found")


@router.put("/{plant_id}", response_model=PlantResponse)
def update_plant(plant_id: int, plant: PlantCreate, db: Session = Depends(get_db)):
    try:
        return service.update_plant(db, plant_id, plant)
    except Exception:
        raise HTTPException(status_code=404, detail="Plant not found")


@router.delete("/{plant_id}")
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    try:
        service.delete_plant(db, plant_id)
        return {"message": "Plant deleted successfully"}
    except Exception:
        raise HTTPException(status_code=404, detail="Plant not found")