from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from core.db import get_db,Base, engine
from schemas.tasks_schemas import TaskCreate, TaskResponse, TaskUpdate
from repository.tasks_repo import Task
from service import task_service



Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/tasks", tags=["Tasks"])



@router.get("/")
def read_root():
    return {"message": "Server is running and tables are created!"}

@router.get("/tasks", response_model=list[TaskResponse])
def get_all_tasks(task: TaskResponse = Depends(get_db)):
    return task_service.list_all_tasks(task)   
  
  

@router.post("/tasks/", response_model=TaskCreate)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_new_task(db, task)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    updated = task_service.update_task(db, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = task_service.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}