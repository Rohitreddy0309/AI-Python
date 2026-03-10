from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.utils.rate_limiter import rate_limiter
from app.services.file_service import FileService
from app.schemas.file import FileResponse
from app.core.database import SessionLocal

router = APIRouter()
file_service = FileService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Upload file
@router.post("/upload", response_model=FileResponse, dependencies=[Depends(rate_limiter)])
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    db_file = await file_service.save_file(db, file)
    return  db_file

# Show all files
@router.get("/files", response_model=list[FileResponse])
def get_files(db: Session = Depends(get_db)):
    return file_service.get_files(db)


# Delete file
@router.delete("/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    return file_service.delete_file(db, file_id)



