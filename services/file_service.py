"""
Utility functions for handling file uploads.

This module provides asynchronous functionality to save uploaded files
to the server using aiofiles for non-blocking file I/O operations.
"""

import os

import aiofiles
from fastapi import UploadFile

UPLOAD_DIR = "uploads"


async def save_file(file: UploadFile):
    """
    Save an uploaded file asynchronously to the uploads directory.

    This function ensures the upload directory exists, reads the file
    content asynchronously, writes it to disk, and returns the file path
    along with the file size.

    Args:
        file (UploadFile): The uploaded file received from the client.

    Returns:
        tuple: A tuple containing the saved file path and the size of the file in bytes.
    """

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    async with aiofiles.open(file_path, "wb") as buffer:

        content = await file.read()

        await buffer.write(content)

    return file_path, len(content)
