from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import io
import re
import os
import logging
from src.utils.inmemory import db

SCOPES = ['https://www.googleapis.com/auth/drive']
CREDS_PATH = 'credentials.json'

log = logging.getLogger(__name__)

def _get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDS_PATH, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)


def get_file_metadata(file_id: str) -> dict:
    """
    Fetches the metadata for a given file ID.
    """
    service = _get_drive_service()
    return service.files().get(fileId=file_id, fields='id, name, mimeType, shared').execute()


def download_from_drive(cv_id: str, drive_url: str, dest_path: str) -> str:
    """
    Accepts a Google Drive share URL or file ID. Validates PDF type,
    checks public access, and downloads to dest_path.
    """
    # Extract file ID
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', drive_url)
    file_id = match.group(1) if match else drive_url

    service = _get_drive_service()
    try:
        meta = get_file_metadata(file_id)
    except HttpError as e:
        status = e.resp.status
        if status in (403, 404):
            raise PermissionError(f"Cannot access file {file_id}: HTTP {status}")
        raise

    # Only allow PDFs
    if meta.get('mimeType') != 'application/pdf':
        raise ValueError(f"File '{meta.get('name')}' is not a PDF. Detected type: {meta.get('mimeType')}")

    # Ensure the file is publicly shared or accessible
    if not meta.get('shared'):
        # If it's not shared, attempt to set shareable link (optional)
        # For now, reject
        raise PermissionError(f"File '{meta.get('name')}' is not shared publicly.")

    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(dest_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.close()
    if not os.path.exists(dest_path):
        db.set(f"{cv_id}", {
            "status": "failed",
        })
        raise Exception("PDF download failed.")
    return dest_path

def upload_to_drive(cv_id: str, file_path: str) -> str:
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json', scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': 'cv.pdf'}
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    file_id = file.get('id')
    if not file_id:
        db.set(f"{cv_id}", {
            "status": "failed",
        })
        raise Exception("PDF upload failed.")
    # make the file publicly readable
    try:
        service.permissions().create(
            fileId=file_id,
            body={
                'type': 'anyone',
                'role': 'reader',
                'allowFileDiscovery': False
            }
        ).execute()
        log.info(f"Set public 'anyone' reader permission on file {file_id}")
    except HttpError as e:
        log.warning(f"Could not set public permission for {file_id}: {e}")
    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
