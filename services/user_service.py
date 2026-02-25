from sqlalchemy.orm import Session
from repositories import user_repository
from Schemas.user import UsersCreate, UsersUpdate


def list_all_users(db: Session):
    return user_repository.get_all_users(db)


def get_by_id(db: Session, id: int):
    return user_repository.get_user_by_id(db, id)


def new_user(db: Session, user_data: UsersCreate):
    return user_repository.add_user(db, user_data)


def details_update(db: Session, id: int, updated_data: UsersUpdate):
    return user_repository.update_user(db, id, updated_data)


def user_delete(db: Session, id: int):
    return user_repository.delete_user(db, id)