from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db
from services.student_service import StudentService
from repositories.student_repository import StudentRepository


def get_student_service(db: Session = Depends(get_db)):

    repository = StudentRepository(db)

    service = StudentService(repository)

    return service