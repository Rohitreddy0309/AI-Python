from sqlalchemy.orm import Session
from models.user import User
from Schemas.user import UsersCreate, UsersUpdate, UsersBulkUpdate
from utils.exceptions import UserNotFoundException, DuplicateEmailException
import os

UPLOAD_FOLDER = "uploads"


def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise UserNotFoundException()

    return user


def add_user_with_photo(db: Session, name, email, department, filename):

    existing_user = db.query(User)\
        .filter(User.email == email.strip())\
        .first()

    if existing_user:
        raise DuplicateEmailException()

    new_user = User(
        name=name,
        email=email.strip(),
        department=department,
        photo=filename
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def update_user_with_photo(db: Session, id: int, name, email, department, filename):

    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise UserNotFoundException()

    if name:
        user.name = name

    if email:
        email = email.strip()

        existing_user = db.query(User)\
            .filter(User.email == email)\
            .filter(User.id != id)\
            .first()

        if existing_user:
            raise DuplicateEmailException()

        user.email = email

    if department:
        user.department = department

   
    if filename:
       
        if user.photo:
            old_path = os.path.join(UPLOAD_FOLDER, user.photo)
            if os.path.exists(old_path):
                os.remove(old_path)

        user.photo = filename

    db.commit()
    db.refresh(user)

    return user


def delete_user_with_photo(db: Session, id: int):

    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise UserNotFoundException()

   
    if user.photo:
        file_path = os.path.join(UPLOAD_FOLDER, user.photo)
        if os.path.exists(file_path):
            os.remove(file_path)

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


def bulk_create_users(db: Session, users: list[UsersCreate]):

    user_objects = []

    for user in users:
        user_obj = User(**user.model_dump())
        user_objects.append(user_obj)

    db.add_all(user_objects)
    db.commit()

    for user in user_objects:
        db.refresh(user)

    return user_objects


def bulk_update_users(db: Session, users: list[UsersBulkUpdate]):

    updated_users = []

    for user_data in users:
        user = db.query(User).filter(User.id == user_data.id).first()

        if not user:
            continue

        update_dict = user_data.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            if key != "id":
                setattr(user, key, value)

        updated_users.append(user)

    db.commit()

    return updated_users