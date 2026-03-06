from sqlalchemy.orm import Session
from fastapi import UploadFile, BackgroundTasks, Request
from models.user import User
from repositories import user_repository
from utils.exceptions import UserNotFoundException, DuplicateEmailException
from Schemas.user import UsersBulkUpdate
import os
import shutil

from core.config import settings

UPLOAD_FOLDER = settings.UPLOAD_FOLDER

def save_photo(photo: UploadFile):

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, photo.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    return photo.filename


def generate_photo_url(request: Request, filename):

    if filename:
        return str(request.url_for("uploads", path=filename))

    return None

def list_all_users(db: Session, request: Request):

    users = user_repository.get_all_users(db)

    for user in users:
        user.photo = generate_photo_url(request, user.photo)

    return users

def get_user(db: Session, user_id: int, request: Request):

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
    photo: UploadFile
):

    email = email.strip()

    existing_user = user_repository.get_user_by_email(db, email)

    if existing_user:
        raise DuplicateEmailException()

    filename = None

    if photo:
        filename = save_photo(photo)

    new_user = User(
        name=name,
        email=email,
        department=department,
        photo=filename
    )

    return user_repository.create_user(db, new_user)


def update_user_service(
    db: Session,
    user_id: int,
    name,
    email,
    department,
    photo: UploadFile
):

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