from sqlalchemy.orm import Session
from schemas.tasks_schemas import TaskCreate, TaskUpdate
from models.tasks import Task



# CRUD operations for Task model

def get_all_tasks(db: Session):
    return db.query(Task).all()

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, task: TaskCreate):
    new_task = Task(title=task.title,description=task.description,completed=task.completed)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None
    for key, value in task_data.model_dump().items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None
    db.delete(db_task)
    db.commit()
    return db_task