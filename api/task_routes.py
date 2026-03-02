from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from core.db import get_db,Base, engine
from schemas.tasks_schemas import TaskCreate, TaskResponse, TaskUpdate
from repository import tasks_repo
from service import task_service
from core.config import logger


Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/tasks", tags=["Tasks"])



@router.get("/")
def read_root():
    return {"message": "Server is running and tables are created!"}

@router.get("/tasks", response_model=list[TaskResponse])
def get_all_tasks(task: TaskResponse = Depends(get_db)):
    logger.info("Received request to fetch all tasks")
    tasks = task_service.list_all_tasks(task)
    if not tasks:
        logger.warning("No tasks found in the database")
        raise HTTPException(status_code=404, detail="No tasks found")
    logger.info(f"Returning {len(tasks)} tasks")
    return tasks
  
  

@router.post("/tasks/", response_model=TaskCreate)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    logger.info(f"Received request to create task with data: {task}")

    created_task = task_service.create_new_task(db, task)
    if not created_task:
        logger.error("Failed to create task")
        raise HTTPException(status_code=500, detail="Failed to create task")
    logger.info(f"Task created successfully: {created_task.title}")
    return created_task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    logger.info(f"Received request to update task with ID: {task_id} and data: {task}")
    updated = task_service.update_task(db, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Task updated successfully: {updated.title}")
    return updated

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received request to delete task with ID: {task_id}")
    deleted = task_service.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Task deleted successfully with ID: {task_id}")
    return {"detail": "Task deleted successfully"}