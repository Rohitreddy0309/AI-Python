from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Depends
from sqlalchemy.orm import Session
import os
import time

from database import engine, get_db, SessionLocal
from models import Base, UploadedFile

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------------------
# Background Processing Function  |
# ---------------------------------
def process_file(file_id: int):
    db = SessionLocal()

    # Simulate long processing
    time.sleep(5)

    file_record = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
    if file_record:
        file_record.status = "completed"
        db.commit()

    db.close()

# -----------------------------
# Upload Endpoint
# -----------------------------
@app.post("/upload")
def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save file locally
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Save metadata in DB
    db_file = UploadedFile(
        filename=file.filename,
        status="processing"
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    # Run background task
    background_tasks.add_task(process_file, db_file.id)

    return db_file

# -----------------------------
# Check File Status
# -----------------------------
@app.get("/files/{file_id}")
def get_file_status(file_id: int, db: Session = Depends(get_db)):
    file_record = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()

    if not file_record:
        return "File not found"
    return file_record