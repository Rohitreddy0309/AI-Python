from sqlalchemy.orm import Session
from repository import tasks_repo as repo
from schemas.tasks_schemas import TaskCreate, TaskUpdate

def list_all_tasks(db: Session):
    return repo.get_all_tasks(db)

def create_new_task(db: Session, task: TaskCreate):    
    return repo.create_task(db, task)

def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    return repo.update_task(db, task_id, task_data)

def delete_task(db: Session, task_id: int):
    return repo.delete_task(db, task_id)