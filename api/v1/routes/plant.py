from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from services.plant_services import PlantService
from schemas.schemas import PlantCreate, PlantResponse, PlantUpdate, PlantBulkUpdate
from fastapi import UploadFile, File, Depends, HTTPException
import os
import shutil
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
def patch_plant(plant_id: int,plant: PlantUpdate,db: Session = Depends(get_db)):
    return service.patch_plant(db, plant_id, plant)

@router.put("/bulk", response_model=list[PlantResponse])
def update_plants_bulk(plants: list[PlantBulkUpdate],
                       db: Session = Depends(get_db)):
    return service.update_plants_bulk(db, plants)
           
@router.post("/{plant_id}/upload-image")
async def upload_plant_image(plant_id: int, 
                             file: UploadFile = File(...),
                             db: Session =Depends(get_db)):
    plant = service.get_plant(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="plant not found")
    
    ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "video/mp4","video/mpeg","audio/mpeg", "application/pdf"]
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")    
    
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    plant.image_url = file_path
    db.commit()
    db.refresh(plant)
    
    return {"message": "Image Uploaded successfully", "image_url": file_path}

 
        
          