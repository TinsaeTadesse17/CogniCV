from fastapi import APIRouter, Form, Response, UploadFile, File, BackgroundTasks
from src.services import parser, llm, compiler, drive
from src.utils.file_ops import temp_file_path
from src.utils.inmemory import db
import uuid
from dotenv import load_dotenv
import csv, io

load_dotenv()

router = APIRouter()

@router.post("/upload")
def upload_cv(
    response: Response,
    drive_link: str = Form(...)
):
    random_id = str(uuid.uuid4())
    local_pdf = temp_file_path(suffix=".pdf")
    drive.download_from_drive(random_id, drive_link, local_pdf)
    
    raw_text = parser.parse_text(local_pdf)

    db.set(f"{random_id}",{
        "status": "processing",
    }),

    structured_data = llm.extract_structured_data(raw_text)
    pdf_path = compiler.compile_latex_string_to_pdf(structured_data)
    new_drive_url = drive.upload_to_drive(random_id, pdf_path)
    db.set(f"{random_id}",{
        "drive_url": new_drive_url,
        "status": "Done",
    }),

    response.status_code = 202
    return {"success": True, 
            "cv_id": random_id,
            "status": "Done"}

@router.post("/batch_upload")
async def batch_upload(
    background_tasks: BackgroundTasks,
    csv_file: UploadFile = File(...)
):
    """
    Accepts a CSV file with a 'cv_link' column and processes each CV in the background.
    Returns a list of job IDs.
    """
    content = await csv_file.read()
    text_stream = io.StringIO(content.decode('utf-8'))
    reader = csv.DictReader(text_stream)
    job_ids = []
    for row in reader:
        cv_link = row.get('cv-link')
        print("Processing CV link:", cv_link)
        if cv_link:
            cv_id = str(uuid.uuid4())
            db.set(cv_id, { 'status': 'pending' })
            background_tasks.add_task(_process_cv_job, cv_id, cv_link)
            job_ids.append(cv_id)  
    return { 'success': True, 'job_ids': job_ids }

def _process_cv_job(cv_id: str, drive_link: str):
    """Helper to download, parse, generate, compile, and upload a single CV, updating db status."""
    try:
        # Download PDF
        local_pdf = temp_file_path(suffix='.pdf')
        drive.download_from_drive(cv_id, drive_link, local_pdf)
        # Parse, extract
        raw_text = parser.parse_text(local_pdf)
        db.set(cv_id, { 'status': 'processing' })
        structured = llm.extract_structured_data(raw_text)
        # Generate PDF
        pdf_path = compiler.compile_latex_string_to_pdf(structured)
        # Upload to Drive
        new_url = drive.upload_to_drive(cv_id, pdf_path)
        db.set(cv_id, { 'status': 'Done', 'drive_url': new_url })
    except Exception as e:
        db.set(cv_id, { 'status': 'failed', 'error': str(e) })
        return

@router.get("/status/{cv_id}")
def get_status(response: Response, cv_id: str):
    """
    Fetches the status of a job using its ID.
    """
    cur_cv = db.get(cv_id)
    if not cur_cv:
        response.status_code = 404
        return {"sucess": False, 
            "error": "CV ID not found."}
    if cur_cv["status"] == "pending":
        response.status_code = 202
        return {"success": True, "status": "pending"}
    elif cur_cv["status"] == "processing":
        response.status_code = 202
        return {"success": True, "status": "processing"}
    elif cur_cv["status"] == "Done":
        response.status_code = 200
        return {"success": True, "drive_url": cur_cv["drive_url"]}
    
    response.status_code = 500
    return {"success": False,
        "error": "Unexpected status value."}

