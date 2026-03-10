import os

import aiofiles
from fastapi import UploadFile

UPLOAD_DIR = "uploads"


async def save_file(file: UploadFile):

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    async with aiofiles.open(file_path, "wb") as buffer:

        content = await file.read()

        await buffer.write(content)

    return file_path, len(content)
