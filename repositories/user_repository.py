from sqlalchemy.orm import Session
from model.user import User


class UserRepository:

    def create(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def list_all(self, db: Session):
        return db.query(User).all()

    def update(self, db: Session, user: User):
        db.commit()
        db.refresh(user)
        return user