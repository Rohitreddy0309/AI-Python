from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from dependencies.plant_dependencies import get_plant_service
from services.plant_services import PlantService
from schemas.schemas import PlantCreate, PlantResponse, PlantUpdate, PlantBulkUpdate
from utils.rate_limiter import rate_limiter

import aiofiles
import asyncio
import os

router = APIRouter()

UPLOAD_FOLDER = "uploads"


@router.post("/", response_model=PlantResponse)
def create_plant(
    plant: PlantCreate,
    service: PlantService = Depends(get_plant_service),
    _: None = Depends(rate_limiter)
):
    return service.create_plant(plant)


@router.get("/", response_model=list[PlantResponse])
def get_plants(service: PlantService = Depends(get_plant_service)):
    return service.get_plants()


@router.get("/{plant_id}", response_model=PlantResponse)
def get_plant(
    plant_id: int,
    service: PlantService = Depends(get_plant_service)
):
    return service.get_plant(plant_id)


@router.put("/{plant_id}", response_model=PlantResponse)
def update_plant(
    plant_id: int,
    plant: PlantCreate,
    service: PlantService = Depends(get_plant_service)
):
    return service.update_plant(plant_id, plant)


@router.delete("/bulk")
def bulk_delete_plants(
    plants_ids: list[int],
    service: PlantService = Depends(get_plant_service)
):
    service.bulk_delete_plants(plants_ids)
    return {"message": "Plants deleted successfully"}


@router.delete("/{plant_id}")
def delete_plant(
    plant_id: int,
    service: PlantService = Depends(get_plant_service)
):
    service.delete_plant(plant_id)
    return {"message": "Plant deleted successfully"}


@router.post("/bulk", response_model=list[PlantResponse])
def create_plants_bulk(
    plants: list[PlantCreate],
    service: PlantService = Depends(get_plant_service)
):
    return service.create_plants_bulk(plants)


@router.patch("/{plant_id}", response_model=PlantResponse)
def patch_plant(
    plant_id: int,
    plant: PlantUpdate,
    service: PlantService = Depends(get_plant_service)
):
    return service.patch_plant(plant_id, plant)


@router.put("/bulk", response_model=list[PlantResponse])
def update_plants_bulk(
    plants: list[PlantBulkUpdate],
    service: PlantService = Depends(get_plant_service)
):
    return service.bulk_update_plants(plants)


@router.post("/upload/{plant_id}")
async def upload_file(
    plant_id: int,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    service: PlantService = Depends(get_plant_service)
):

    plant = service.get_plant(plant_id)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    plant.file_path = file_path
    plant.file_status = "PENDING"

    service.db.commit()

    background_tasks.add_task(process_file, file_path, plant_id)

    return {
        "message": "File uploaded successfully",
        "status": "processing started in background"
    }


async def process_file(file_path: str, plant_id: int):

    print("Processing started...")

    await asyncio.sleep(5)

    with open(file_path, "rb") as f:
        content = f.read()

    file_size = len(content)

    result = f"File processed successfully. Size: {file_size} bytes"

    print("Processing finished:", result)