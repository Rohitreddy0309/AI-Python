from sqlalchemy.orm import Session
from app.models.file import File


class FileRepository:

    def create_file(self, db: Session, file_id: int, filename: str, filepath: str):

        db_file = File(
            id=file_id,
            filename=filename,
            filepath=filepath
    )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return db_file

    def get_all_files(self, db: Session):
        return db.query(File).all()

    def get_file(self, db: Session, file_id: int):
        return db.query(File).filter(File.id == file_id).first()

    def delete_file(self, db: Session, file):
        db.delete(file)
        db.commit()