"""Task API routes.

Defines FastAPI endpoints for task CRUD operations and file uploads.
Business logic is delegated to :class:`~service.task_service.TaskService`
through dependency injection.
"""

import asyncio
import os

import aiofiles
from fastapi import (APIRouter, BackgroundTasks, Depends, File, HTTPException,
                     UploadFile)

from core.config import logger
from dependencies.task_dependencies import get_task_service
from schemas.tasks_schemas import TaskCreate, TaskResponse, TaskUpdate
from service.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(service: TaskService = Depends(get_task_service)):
    """Return a list of all tasks."""

    logger.info("Fetching all tasks")

    tasks = service.list_all_tasks()

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")

    return tasks


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service)):
    """Create a new task."""

    logger.info("Creating new task")

    created_task = service.create_new_task(task)

    return created_task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, task: TaskUpdate, service: TaskService = Depends(get_task_service)
):
    """Update an existing task by ID."""

    updated = service.update_task(task_id, task)

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated


@router.delete("/{task_id}")
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """Delete a task by ID."""

    deleted = service.delete_task(task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


async def process_file(file_path: str):
    """Simulate processing a file in the background."""

    await asyncio.sleep(5)
    logger.info("Finished processing file: %s", file_path)


@router.post("/{task_id}/upload")
async def upload_file(
    task_id: int,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    service: TaskService = Depends(get_task_service),
):
    """Upload a file for a task and queue background processing."""

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = f"{upload_dir}/{file.filename}"

    content = await file.read()

    async with aiofiles.open(file_path, "wb") as out_file:
        await out_file.write(content)

    # Persist the uploaded filename to the task record
    task = service.attach_file_to_task(task_id, file.filename)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    background_tasks.add_task(process_file, file_path)

    return {
        "message": "File uploaded successfully",
        "task_id": task_id,
        "file_name": file.filename,
    }
