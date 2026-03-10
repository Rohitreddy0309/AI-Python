"""
API router for user-related endpoints.

This module defines all HTTP routes for user management including
fetching users, creating users with photo upload, updating users,
deleting users, and performing bulk operations.
"""

from fastapi import (APIRouter, BackgroundTasks, Depends, File, Form, Request,
                     UploadFile)
from sqlalchemy.orm import Session

from core.database import get_db
from Schemas.user import UserResponse, UsersBulkUpdate, UsersCreate
from services import user_service
from utils.rate_limiter import rate_limiter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/api/v1/users", response_model=list[UserResponse])
def get_all_users(request: Request, db: Session = Depends(get_db)):
    """
    Retrieve all users.

    Args:
        request (Request): FastAPI request object.
        db (Session): Database session dependency.

    Returns:
        list[UserResponse]: List of users with their details.
    """
    return user_service.list_all_users(db, request)


@router.get("/api/v1/users/get/{id}", response_model=UserResponse)
def get_user_by_id(id: int, request: Request, db: Session = Depends(get_db)):
    """
    Retrieve a single user by ID.

    Args:
        id (int): ID of the user.
        request (Request): FastAPI request object.
        db (Session): Database session dependency.

    Returns:
        UserResponse: User details.
    """
    return user_service.get_by_id(db, id, request)


@router.post("/add", response_model=UserResponse)
def add_user(
    background_tasks: BackgroundTasks,
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    department: str = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Create a new user with photo upload.

    Applies rate limiting based on the client's IP address.

    Args:
        background_tasks (BackgroundTasks): Background task manager.
        request (Request): FastAPI request object.
        name (str): User name.
        email (str): User email.
        department (str): User department.
        photo (UploadFile): Uploaded user photo.
        db (Session): Database session dependency.

    Returns:
        UserResponse: Created user details.
    """
    rate_limiter(request.client.host)

    return user_service.new_user_with_photo(
        db, background_tasks, name, email, department, photo
    )


@router.put("/update/{id}", response_model=UserResponse)
def update_user(
    id: int,
    background_tasks: BackgroundTasks,
    name: str = Form(None),
    email: str = Form(None),
    department: str = Form(None),
    photo: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    """
    Update an existing user and optionally update their photo.

    Args:
        id (int): ID of the user to update.
        background_tasks (BackgroundTasks): Background task manager.
        name (str | None): Updated name.
        email (str | None): Updated email.
        department (str | None): Updated department.
        photo (UploadFile | None): Updated photo file.
        db (Session): Database session dependency.

    Returns:
        UserResponse: Updated user details.
    """

    return user_service.update_user_with_photo(
        db, background_tasks, id, name, email, department, photo
    )


@router.get("/api/v1/users/delete/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    """
    Delete a user by ID.

    Args:
        id (int): ID of the user to delete.
        db (Session): Database session dependency.

    Returns:
        dict: Confirmation message.
    """
    return user_service.user_delete(db, id)


@router.post("/api/v1/users/bulk", response_model=list[UserResponse])
def bulk_create_users(users: list[UsersCreate], db: Session = Depends(get_db)):
    """
    Create multiple users in a single request.

    Args:
        users (list[UsersCreate]): List of user creation data.
        db (Session): Database session dependency.

    Returns:
        list[UserResponse]: List of created users.
    """
    return user_service.bulk_create_users_service(db, users)


@router.patch("/api/v1/users/bulk", response_model=list[UserResponse])
def bulk_update_users(users: list[UsersBulkUpdate], db: Session = Depends(get_db)):
    """
    Update multiple users in a single request.

    Args:
        users (list[UsersBulkUpdate]): List of user update data.
        db (Session): Database session dependency.

    Returns:
        list[UserResponse]: List of updated users.
    """
    return user_service.bulk_update_users_service(db, users)
