import time

from core.database import SessionLocal
from repositories.file_repo import update_file_status


def process_file(file_id: int):

    db = SessionLocal()

    try:

        print("Processing file...")

        time.sleep(5)  # simulate parsing

        parsed_result = "File parsed successfully"

        update_file_status(db, file_id, "completed", parsed_result)

    except Exception as e:

        update_file_status(db, file_id, "processing_failed", str(e))

    finally:

        db.close()
