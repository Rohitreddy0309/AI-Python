from sqlalchemy.orm import Session
from model.user import User
from repositories.user_repository import UserRepository
from schemas.user import UserCreate, UserUpdate
from utils.exceptions import NotFoundException, ConflictException


class UserService:

    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        existing_user = self.repository.get_by_email(db, user_data.email)
        if existing_user:
            raise ConflictException("Email already exists")

        user = User(
            name=user_data.name,
            email=user_data.email,
        )
        return self.repository.create(db, user)

    def get_user(self, db: Session, user_id: int) -> User:
        user = self.repository.get_by_id(db, user_id)
        if not user:
            raise NotFoundException("User not found")
        return user

    def list_users(self, db: Session):
        return self.repository.list_all(db)

    def update_user(self, db: Session, user_id: int, user_data: UserUpdate):
        user = self.repository.get_by_id(db, user_id)
        if not user:
            raise NotFoundException("User not found")

        if user_data.name is not None:
            user.name = user_data.name

        if user_data.is_active is not None:
            user.is_active = user_data.is_active

        return self.repository.update(db, user)

    def delete_user(self, db: Session, user_id: int):
        user = self.repository.get_by_id(db, user_id)
        if not user:
            raise NotFoundException("User not found")

        user.is_active = False
        return self.repository.update(db, user)