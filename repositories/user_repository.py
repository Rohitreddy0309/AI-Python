from sqlalchemy.orm import Session
from Schemas.user import UsersCreate, UsersUpdate
from models.user import User


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()


def add_user(db: Session, user: UsersCreate):
    existing_user = db.query(User)\
        .filter(User.email == user.email.strip())\
        .first()

    if existing_user:
        return None

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
        return None

    user.name = updated_data.name
    user.email = updated_data.email

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        return None

    db.delete(user)
    db.commit()
    return user