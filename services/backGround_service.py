"""
Background file processing service.

This module contains logic for simulating file parsing and updating
the file processing status in the database.
"""

import time

from core.database import SessionLocal
from repositories.file_repo import update_file_status


def process_file(file_id: int):
    """
    Process an uploaded file in the background.

    This function simulates file parsing by waiting for a few seconds
    and then updates the file status in the database. If an error occurs
    during processing, the status is updated as failed.

    Args:
        file_id (int): ID of the file record stored in the database.
    """

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
