import os
from app.models.file import File
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.repositories.file_repository import FileRepository
from app.core.config import settings


def get_lowest_available_id(db: Session):

    ids = db.query(File.id).order_by(File.id).all()

    expected = 1
    for (id_val,) in ids:
        if id_val != expected:
            return expected
        expected += 1

    return expected

class FileService:

    def __init__(self):
        self.repository = FileRepository()

    async def save_file(self, db: Session, upload_file: UploadFile):
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(settings.UPLOAD_DIR, upload_file.filename)

        contents = await upload_file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        new_id = get_lowest_available_id(db)

        db_file = self.repository.create_file(
            db,
            new_id,
            upload_file.filename,
            file_path
        )

        return db_file

    def get_files(self, db: Session):
        return self.repository.get_all_files(db)

    def delete_file(self, db: Session, file_id: int):

        db_file = self.repository.get_file(db, file_id)

        if not db_file:
            raise HTTPException(status_code=404, detail="File not found")

        if os.path.exists(db_file.filepath):
            os.remove(db_file.filepath)

        self.repository.delete_file(db, db_file)

        return {"message": "File deleted successfully"}