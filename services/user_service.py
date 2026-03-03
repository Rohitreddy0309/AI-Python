from sqlalchemy.orm import Session
from repositories import user_repository
from Schemas.user import UsersBulkUpdate
from fastapi import UploadFile
import os
import shutil

UPLOAD_FOLDER = "uploads"

def save_photo(photo: UploadFile):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, photo.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    return photo.filename

def generate_photo_url(request, filename):
    if filename:
        return str(request.url_for("uploads", path=filename))
    return None

def list_all_users(db: Session, request):
    users = user_repository.get_all_users(db)

    for user in users:
        user.photo = generate_photo_url(request, user.photo)

    return users

def get_by_id(db: Session, id: int, request):
    user = user_repository.get_user_by_id(db, id)
    user.photo = generate_photo_url(request, user.photo)
    return user



def new_user_with_photo(db: Session, name, email, department, photo: UploadFile):
    filename = save_photo(photo)

    return user_repository.add_user_with_photo(
        db, name, email, department, filename
    )

def update_user_with_photo(db: Session, id: int, name, email, department, photo: UploadFile):

    filename = None

    if photo:
        filename = save_photo(photo)

    return user_repository.update_user_with_photo(
        db, id, name, email, department, filename
    )


def user_delete(db: Session, id: int):
    return user_repository.delete_user_with_photo(db, id)


def bulk_create_users_service(db: Session, users):
    emails = [user.email.strip() for user in users]

    if len(emails) != len(set(emails)):
        return {"message": "Duplicate emails in request"}

    return user_repository.bulk_create_users(db, users)

def bulk_update_users_service(db: Session, users: list[UsersBulkUpdate]):

    if not users:
        return {"message": "Empty update list"}

    return user_repository.bulk_update_users(db, users)