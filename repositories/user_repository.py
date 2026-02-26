from sqlalchemy.orm import Session
from Schemas.user import UsersCreate, UsersUpdate
from models.user import User
from utils.exceptions import UserNotFoundException, DuplicateEmailException


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise UserNotFoundException()

    return user


def add_user(db: Session, user: UsersCreate):
    existing_user = db.query(User)\
        .filter(User.email == user.email.strip())\
        .first()

    if existing_user:
        raise DuplicateEmailException()

    new_user = User(
        **user.model_dump(exclude={"id", "createdAt"})
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, id: int, updated_data: UsersUpdate):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise UserNotFoundException()

    # Optional: check duplicate email during update
    existing_user = db.query(User)\
        .filter(User.email == updated_data.email.strip())\
        .filter(User.id != id)\
        .first()

    if existing_user:
        raise DuplicateEmailException()

    user.name = updated_data.name
    user.email = updated_data.email.strip()

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise UserNotFoundException()

    db.delete(user)
    db.commit()
    return user