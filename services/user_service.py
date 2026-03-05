from sqlalchemy.orm import Session
from repositories import user_repository
from repositories import file_repo
from Schemas.user import UsersBulkUpdate
from fastapi import UploadFile, BackgroundTasks
from services.backGround_service import process_file
import os
import shutil

UPLOAD_FOLDER = "uploads"

def save_photo(photo: UploadFile):

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, photo.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    file_size = os.path.getsize(file_path)

    return photo.filename, file_path, file_size

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

def new_user_with_photo(
    db: Session,
    background_tasks,
    name,
    email,
    department,
    photo: UploadFile
):

    try:
        filename, file_path, file_size = save_photo(photo)

        user = user_repository.add_user_with_photo(
            db, name, email, department, filename
        )

        file_repo.create_file_record(
            db,
            {
                "id": user.id,
                "file_name": filename,
                "file_path": file_path,
                "file_size": file_size,
                "upload_status": "uploaded"
            }
        )

        background_tasks.add_task(process_file, user.id)

        return user   

    except Exception as e:
        print("Upload failed:", e)

        # still return user if created
        user = user_repository.add_user_with_photo(
            db, name, email, department, None
        )

        return user

def update_user_with_photo(
    db: Session,
    background_tasks: BackgroundTasks,
    id: int,
    name,
    email,
    department,
    photo: UploadFile
):

    filename = None
    file_path = None
    file_size = None

    if photo:

        filename, file_path, file_size = save_photo(photo)

        file_repo.create_file_record(
            db,
            {
                "id": id,
                "file_name": filename,
                "file_path": file_path,
                "file_size": file_size,
                "upload_status": "uploaded"
            }
        )

        background_tasks.add_task(process_file, id)

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
