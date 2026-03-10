from fastapi import (APIRouter, BackgroundTasks, Depends, File, Form, Request,
                     UploadFile)
from sqlalchemy.orm import Session

from core.database import get_db
from Schemas.user import UserResponse, UsersBulkUpdate, UsersCreate
from services import user_service
from utils.rate_limiter import rate_limiter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/api/v1/users", response_model=list[UserResponse])
def get_all_users(request: Request, db: Session = Depends(get_db)):
    return user_service.list_all_users(db, request)


@router.get("/api/v1/users/get/{id}", response_model=UserResponse)
def get_user_by_id(id: int, request: Request, db: Session = Depends(get_db)):
    return user_service.get_by_id(db, id, request)


@router.post("/add", response_model=UserResponse)
def add_user(
    background_tasks: BackgroundTasks,
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    department: str = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    rate_limiter(request.client.host)

    return user_service.new_user_with_photo(
        db, background_tasks, name, email, department, photo
    )


@router.put("/update/{id}", response_model=UserResponse)
def update_user(
    id: int,
    background_tasks: BackgroundTasks,
    name: str = Form(None),
    email: str = Form(None),
    department: str = Form(None),
    photo: UploadFile = File(None),
    db: Session = Depends(get_db),
):

    return user_service.update_user_with_photo(
        db, background_tasks, id, name, email, department, photo
    )


@router.get("/api/v1/users/delete/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    return user_service.user_delete(db, id)


@router.post("/api/v1/users/bulk", response_model=list[UserResponse])
def bulk_create_users(users: list[UsersCreate], db: Session = Depends(get_db)):
    return user_service.bulk_create_users_service(db, users)


@router.patch("/api/v1/users/bulk", response_model=list[UserResponse])
def bulk_update_users(users: list[UsersBulkUpdate], db: Session = Depends(get_db)):
    return user_service.bulk_update_users_service(db, users)
