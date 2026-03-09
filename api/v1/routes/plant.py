"""
Plant API routes.

This module defines REST endpoints for managing plant records,
including CRUD operations, bulk operations, and file uploads
with background processing.
"""

import asyncio
import os

import aiofiles
from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile

from dependencies.plant_dependencies import get_plant_service
from schemas.schemas import PlantBulkUpdate, PlantCreate, PlantResponse, PlantUpdate
from services.plant_services import PlantService
from utils.rate_limiter import rate_limiter

router = APIRouter()

UPLOAD_FOLDER = "uploads"


@router.post("/", response_model=PlantResponse)
def create_plant(
    plant: PlantCreate,
    service: PlantService = Depends(get_plant_service),
    _: None = Depends(rate_limiter),
):
    """Create a new plant record."""
    return service.create_plant(plant)


@router.get("/", response_model=list[PlantResponse])
def get_plants(service: PlantService = Depends(get_plant_service)):
    """Retrieve all plant records."""
    return service.get_plants()


@router.get("/{plant_id}", response_model=PlantResponse)
def get_plant(
    plant_id: int,
    service: PlantService = Depends(get_plant_service),
):
    """Retrieve a plant by its ID."""
    return service.get_plant(plant_id)


@router.put("/{plant_id}", response_model=PlantResponse)
def update_plant(
    plant_id: int,
    plant: PlantCreate,
    service: PlantService = Depends(get_plant_service),
):
    """Update an existing plant record."""
    return service.update_plant(plant_id, plant)


@router.delete("/bulk")
def bulk_delete_plants(
    plants_ids: list[int],
    service: PlantService = Depends(get_plant_service),
):
    """Delete multiple plants by their IDs."""
    service.bulk_delete_plants(plants_ids)
    return {"message": "Plants deleted successfully"}


@router.delete("/{plant_id}")
def delete_plant(
    plant_id: int,
    service: PlantService = Depends(get_plant_service),
):
    """Delete a plant by its ID."""
    service.delete_plant(plant_id)
    return {"message": "Plant deleted successfully"}


@router.post("/bulk", response_model=list[PlantResponse])
def create_plants_bulk(
    plants: list[PlantCreate],
    service: PlantService = Depends(get_plant_service),
):
    """Create multiple plant records in bulk."""
    return service.create_plants_bulk(plants)


@router.patch("/{plant_id}", response_model=PlantResponse)
def patch_plant(
    plant_id: int,
    plant: PlantUpdate,
    service: PlantService = Depends(get_plant_service),
):
    """Partially update a plant record."""
    return service.patch_plant(plant_id, plant)


@router.put("/bulk", response_model=list[PlantResponse])
def update_plants_bulk(
    plants: list[PlantBulkUpdate],
    service: PlantService = Depends(get_plant_service),
):
    """Update multiple plant records in bulk."""
    return service.bulk_update_plants(plants)


@router.post("/upload/{plant_id}")
async def upload_file(
    plant_id: int,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    service: PlantService = Depends(get_plant_service),
):
    """Upload a file for a specific plant and process it asynchronously."""
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
        "status": "processing started in background",
    }


async def process_file(file_path: str, _plant_id: int):
    """Simulate background processing of an uploaded file."""
    print("Processing started...")

    await asyncio.sleep(5)

    with open(file_path, "rb") as f:
        content = f.read()

    file_size = len(content)
    result = f"File processed successfully. Size: {file_size} bytes"

    print("Processing finished:", result)
