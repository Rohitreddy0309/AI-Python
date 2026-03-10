"""
Service layer for user-related operations.

This module contains business logic for user management such as
creating, updating, deleting, and retrieving users. It also handles
photo uploads, URL generation for user photos, and bulk operations.
"""

import os
import shutil

from fastapi import BackgroundTasks, Request, UploadFile
from sqlalchemy.orm import Session

from core.config import settings
from models.user import User
from repositories import user_repository
from Schemas.user import UsersBulkUpdate
from utils.exceptions import DuplicateEmailException, UserNotFoundException

UPLOAD_FOLDER = settings.UPLOAD_FOLDER


def save_photo(photo: UploadFile):
    """
    Save the uploaded user photo to the uploads folder.

    Args:
        photo (UploadFile): Uploaded photo file.

    Returns:
        str: Filename of the saved photo.
    """

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, photo.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    return photo.filename


def generate_photo_url(request: Request, filename):
    """
    Generate the accessible URL for a stored user photo.

    Args:
        request (Request): FastAPI request object used to build the URL.
        filename (str): Name of the stored photo file.

    Returns:
        str | None: Full URL to access the photo or None if no filename exists.
    """

    if filename:
        return str(request.url_for("uploads", path=filename))

    return None


def list_all_users(db: Session, request: Request):
    """
    Retrieve all users and attach their photo URLs.

    Args:
        db (Session): Database session.
        request (Request): FastAPI request object.

    Returns:
        list: List of user objects with photo URLs.
    """

    users = user_repository.get_all_users(db)

    for user in users:
        user.photo = generate_photo_url(request, user.photo)

    return users


def get_user(db: Session, user_id: int, request: Request):
    """
    Retrieve a single user by ID and attach the photo URL.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to retrieve.
        request (Request): FastAPI request object.

    Returns:
        User: Retrieved user object.

    Raises:
        UserNotFoundException: If the user does not exist.
    """

    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        raise UserNotFoundException()

    user.photo = generate_photo_url(request, user.photo)

    return user


def create_user_service(
    db: Session,
    background_tasks: BackgroundTasks,
    name: str,
    email: str,
    department: str,
    photo: UploadFile,
):
    """
    Create a new user with optional photo upload.

    Args:
        db (Session): Database session.
        background_tasks (BackgroundTasks): FastAPI background task handler.
        name (str): Name of the user.
        email (str): Email address of the user.
        department (str): Department of the user.
        photo (UploadFile): Optional uploaded photo.

    Returns:
        User: Newly created user record.

    Raises:
        DuplicateEmailException: If the email already exists.
    """

    email = email.strip()

    existing_user = user_repository.get_user_by_email(db, email)

    if existing_user:
        raise DuplicateEmailException()

    filename = None

    if photo:
        filename = save_photo(photo)

    new_user = User(name=name, email=email, department=department, photo=filename)

    return user_repository.create_user(db, new_user)


def update_user_service(
    db: Session, user_id: int, name, email, department, photo: UploadFile
):
    """
    Update user details and optionally update the user photo.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to update.
        name (str): Updated name.
        email (str): Updated email.
        department (str): Updated department.
        photo (UploadFile): Optional updated photo.

    Returns:
        User: Updated user object.

    Raises:
        UserNotFoundException: If the user does not exist.
        DuplicateEmailException: If the updated email already exists.
    """

    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        raise UserNotFoundException()

    if email:
        email = email.strip()

        existing_user = user_repository.get_user_by_email(db, email)

        if existing_user and existing_user.id != user_id:
            raise DuplicateEmailException()

        user.email = email

    if name:
        user.name = name

    if department:
        user.department = department

    if photo:
        filename = save_photo(photo)
        user.photo = filename

    return user_repository.update_user(db, user)


def delete_user_service(db: Session, user_id: int):
    """
    Delete a user and remove their stored photo if it exists.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to delete.

    Returns:
        dict: Confirmation message.

    Raises:
        UserNotFoundException: If the user does not exist.
    """

    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        raise UserNotFoundException()

    if user.photo:

        file_path = os.path.join(UPLOAD_FOLDER, user.photo)

        if os.path.exists(file_path):
            os.remove(file_path)

    user_repository.delete_user(db, user)

    return {"message": "User deleted successfully"}


def bulk_create_users_service(db: Session, users):
    """
    Create multiple users in a single operation.

    Args:
        db (Session): Database session.
        users (list): List of user data objects.

    Returns:
        list | dict: Created users or error message if duplicate emails exist.
    """

    emails = [user.email.strip() for user in users]

    if len(emails) != len(set(emails)):
        return {"message": "Duplicate emails in request"}

    user_objects = []

    for user in users:

        existing_user = user_repository.get_user_by_email(db, user.email)

        if existing_user:
            raise DuplicateEmailException()

        user_obj = User(**user.model_dump())
        user_objects.append(user_obj)

    return user_repository.bulk_create(db, user_objects)


def bulk_update_users_service(db: Session, users: list[UsersBulkUpdate]):
    """
    Update multiple users in a single operation.

    Args:
        db (Session): Database session.
        users (list[UsersBulkUpdate]): List of user update objects.

    Returns:
        list | dict: Updated users or message if update list is empty.

    Raises:
        UserNotFoundException: If any user in the list does not exist.
    """

    if not users:
        return {"message": "Empty update list"}

    updated_users = []

    for user_data in users:

        user = user_repository.get_user_by_id(db, user_data.id)

        if not user:
            raise UserNotFoundException()

        update_data = user_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():

            if key != "id":
                setattr(user, key, value)

        updated_users.append(user)

    return user_repository.bulk_update(db, updated_users)
