from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from core.database import get_db
from services import user_service
from Schemas.user import UserResponse, UsersCreate, UsersUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/api/v1/users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return user_service.list_all_users(db)


@router.get("/api/v1/users/{id}", response_model=UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return user_service.get_by_id(db, id)


@router.post("/api/v1/users", response_model=UserResponse)
def add_user(user: UsersCreate, db: Session = Depends(get_db)):
    return user_service.new_user(db, user)


@router.put("/api/v1/users/{id}", response_model=UserResponse)
def update_user(id: int, user: UsersUpdate, db: Session = Depends(get_db)):
    return user_service.details_update(db, id, user)


@router.delete("/api/v1/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    return user_service.user_delete(db, id)
