from fastapi import APIRouter, Form , Response
from src.services import parser, llm, templater, compiler, drive
from src.utils.file_ops import temp_file_path
from src.utils.inmemory import db
import uuid

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

    structured_data = llm.extract_structured_data(random_id, raw_text)
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

