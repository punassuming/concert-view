import os
from pathlib import Path

import aiofiles
from fastapi import UploadFile


async def save_upload(feed_id: str, file: UploadFile, upload_dir: str) -> str:
    """Save an uploaded file to disk and return the file path."""
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    ext = os.path.splitext(file.filename or "video.mp4")[1] or ".mp4"
    dest = os.path.join(upload_dir, f"{feed_id}{ext}")
    async with aiofiles.open(dest, "wb") as out:
        while chunk := await file.read(1024 * 1024):
            await out.write(chunk)
    return dest
