import tempfile
import os
import uuid

def temp_file_path(suffix: str = "") -> str:
    """
    Returns a unique temp file path in /tmp with optional suffix.
    """
    filename = f"{uuid.uuid4()}{suffix}"
    path = os.path.join(tempfile.gettempdir(), filename)
    # ensure the directory exists (usually /tmp does)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path
