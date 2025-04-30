import os
import uuid
from fastapi import UploadFile

def save_temp_file(upload_file: UploadFile) -> str:
    temp_dir = "/tmp"
    file_id = str(uuid.uuid4())
    file_path = os.path.join(temp_dir, f"{file_id}_{upload_file.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return file_path
