from fastapi import APIRouter, Form, Response, UploadFile, File, BackgroundTasks
from src.services import parser, llm, compiler, drive
from src.utils.file_ops import temp_file_path
from src.utils.inmemory import db
import uuid
import os
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
    # cleanup temp files
    try:
        os.remove(local_pdf)
        os.remove(pdf_path)
    except OSError:
        pass

    response.status_code = 202
    return {"success": True, 
            "cv_id": random_id,
            "drive_url": new_drive_url,
            "status": "Done"}

@router.post("/batch_upload")
async def batch_upload(
    background_tasks: BackgroundTasks,
    csv_file: UploadFile = File(...)
):
    """
    Accepts a CSV file with a 'cv_link' column, assigns a job ID, and processes all CVs in the background.
    Returns the job ID for the CSV processing.
    """
    content = await csv_file.read()
    # Save original CSV to a temp file
    local_csv = temp_file_path(suffix='.csv')
    with open(local_csv, 'wb') as f:
        f.write(content)
    job_id = str(uuid.uuid4())
    db.set(job_id, {'status': 'pending'})
    background_tasks.add_task(_process_csv_job, job_id, local_csv)
    return {'success': True, 'job_id': job_id}

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
        # cleanup temp files
        try:
            os.remove(local_pdf)
            os.remove(pdf_path)
        except OSError:
            pass
    except Exception as e:
        db.set(cv_id, { 'status': 'failed', 'error': str(e) })
        return

def _process_csv_job(job_id: str, csv_path: str):
    """Process all CVs in a CSV: extract each, append drive_url, upload modified CSV."""
    try:
        db.set(job_id, {'status': 'processing'})
        rows = []
        with open(csv_path, newline='') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames + ['drive_url']
            for row in reader:
                link = row.get('cv_link') or row.get('cv-link')
                if not link:
                    row['drive_url'] = ''
                else:
                    cv_uuid = str(uuid.uuid4())
                    local_pdf = temp_file_path(suffix='.pdf')
                    drive.download_from_drive(cv_uuid, link, local_pdf)
                    text = parser.parse_text(local_pdf)
                    structured = llm.extract_structured_data(text)
                    pdf_path = compiler.compile_latex_string_to_pdf(structured)
                    new_url = drive.upload_to_drive(cv_uuid, pdf_path)
                    row['drive_url'] = new_url
                    # cleanup per-cv temp PDF
                    try:
                        os.remove(local_pdf)
                        os.remove(pdf_path)
                    except OSError:
                        pass
                rows.append(row)
        # Write modified CSV
        new_csv = temp_file_path(suffix='.csv')
        with open(new_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        # Upload final CSV with a descriptive name
        csv_url = drive.upload_to_drive(job_id, new_csv, drive_name='processed_csv.csv')
        db.set(job_id, {'status': 'Done', 'csv_drive_url': csv_url})
        # cleanup temp CSVs
        try:
            os.remove(new_csv)
            os.remove(csv_path)
        except OSError:
            pass
    except Exception as e:
        db.set(job_id, {'status': 'failed', 'error': str(e)})

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
        # Return CSV URL if batch job, else individual CV URL
        if 'csv_drive_url' in cur_cv:
            return {"success": True, "csv_drive_url": cur_cv["csv_drive_url"]}
        return {"success": True, "drive_url": cur_cv.get("drive_url")}
    
    response.status_code = 500
    return {"success": False,
        "error": "Unexpected status value."}

