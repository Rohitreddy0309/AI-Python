from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from core.database import get_db, SessionLocal
from model.user import Plant
from services.plant_services import PlantService
from schemas.schemas import PlantCreate, PlantResponse, PlantUpdate, PlantBulkUpdate

import aiofiles
import asyncio
import os
import shutil

router = APIRouter()
service = PlantService()

UPLOAD_FOLDER = "uploads"



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



@router.delete("/bulk")
def bulk_delete_plants(plants_ids: list[int], db: Session = Depends(get_db)):
    service.bulk_delete_plants(db, plants_ids)
    return {"message": "Plants deleted successfully"}



@router.delete("/{plant_id}")
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    try:
        service.delete_plant(db, plant_id)
        return {"message": "Plant deleted successfully"}
    except Exception:
        raise HTTPException(status_code=404, detail="Plant not found")



@router.post("/bulk", response_model=list[PlantResponse])
def create_plants_bulk(plants: list[PlantCreate], db: Session = Depends(get_db)):
    return service.create_plants_bulk(db, plants)



@router.patch("/{plant_id}", response_model=PlantResponse)
def patch_plant(plant_id: int, plant: PlantUpdate, db: Session = Depends(get_db)):
    return service.patch_plant(db, plant_id, plant)



@router.put("/bulk", response_model=list[PlantResponse])
def update_plants_bulk(plants: list[PlantBulkUpdate], db: Session = Depends(get_db)):
    return service.update_plants_bulk(db, plants)



@router.post("/{plant_id}/upload-image")
async def upload_plant_image(
    plant_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    plant = service.get_plant(db, plant_id)

    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    plant.image_url = file_path

    db.commit()
    db.refresh(plant)

    return {
        "message": "Image uploaded successfully",
        "image_url": file_path
    }


@router.post("/upload/{plant_id}")
async def upload_file(
    plant_id: int,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):

    db = SessionLocal()

    plant = db.query(Plant).filter(Plant.id == plant_id).first()

    if not plant:
        db.close()
        raise HTTPException(status_code=404, detail="Plant not found")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    # update DB immediately
    plant.file_name = file.filename
    plant.file_status = "PENDING"

    db.commit()

    # start background processing
    background_tasks.add_task(process_file, file_path, plant_id)

    db.close()

    return {
        "message": "File uploaded successfully",
        "status": "processing started in background"
    }


async def process_file(file_path: str, plant_id: int):

    db = SessionLocal()

    print("Processing started...")

    await asyncio.sleep(5)

    with open(file_path, "rb") as f:
        content = f.read()

    file_size = len(content)

    plant = db.query(Plant).filter(Plant.id == plant_id).first()

    if plant:
        plant.file_status = "COMPLETED"
        plant.file_result = f"File processed successfully. Size: {file_size} bytes"
        db.commit()

    db.close()

    print("Processing finished")