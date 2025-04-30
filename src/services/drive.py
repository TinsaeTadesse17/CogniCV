from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

def upload_to_drive(file_path: str) -> str:
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json', scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': 'cv.pdf'}
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    file_id = file.get('id')
    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
