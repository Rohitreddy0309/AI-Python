from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.tasks_schemas import TaskCreate, TaskUpdate
from models.tasks import Task
from core.config import logger


# CRUD operations for Task model

def get_all_tasks(db: Session):
    logger.debug("Fetching all tasks from the database")
    try:
        tasks= db.query(Task).all()
        logger.info(f"Retrieved {len(tasks)} tasks from DB")
        return tasks
    except Exception as e:
        logger.error(f"Error fetching tasks: {e}")
        return []

def get_task_by_id(db: Session, task_id: int):
    logger.debug(f"Fetching task with ID: {task_id}")
    try:
        tasks= db.query(Task).filter(Task.id == task_id).first()
        if tasks:
            logger.info(f"Task found:{tasks.title}")
        else:
            logger.warning(f"No task found with ID: {task_id}")
        return tasks
    except Exception as e:
        logger.error(f"Error fetching task: {e}")
        return None
    

def create_task(db: Session, task: TaskCreate):
    logger.debug(f"Creating new task with data: {task}")
    try:
        new_task = Task(title=task.title,description=task.description,completed=task.completed)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        logger.info(f"Task created successfully with ID: {new_task.id}")
        return new_task
    except SQLAlchemyError as e:
        logger.error(f"Error creating task: {e}")
        db.rollback()
        return None

def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    logger.debug(f"Updating task with ID: {task_id} using data: {task_data}")
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        logger.warning(f"Task with ID: {task_id} not found for update")
        return None
    try:
        for key, value in task_data.model_dump().items():
            setattr(db_task, key, value)
    
        db.commit()
        db.refresh(db_task)
        logger.info(f"Task with ID: {task_id} updated successfully")
        return db_task
    except SQLAlchemyError as e:
        logger.error(f"Error updating task: {e}")
        db.rollback()
        return None
def delete_task(db: Session, task_id: int):
    logger.debug(f"Deleting task with ID: {task_id}")
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        logger.warning(f"Task with ID: {task_id} not found for deletion")   
        return None
    try:
        db.delete(db_task)
        db.commit()
        logger.info(f"Task with ID: {task_id} deleted successfully")
        return db_task
    except SQLAlchemyError as e:
        logger.error(f"Error deleting task: {e}")
        db.rollback()
        return None