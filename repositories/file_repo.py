from sqlalchemy.orm import Session

from models.file_data import FileData


def create_file_record(db: Session, file_data: dict):

    file = FileData(**file_data)

    db.add(file)
    db.commit()
    db.refresh(file)

    return file


def update_file_status(db: Session, file_id: int, status: str, result=None):

    file = db.query(FileData).filter(FileData.id == file_id).first()

    if file:
        file.upload_status = status
        file.parsed_result = result
        db.commit()
