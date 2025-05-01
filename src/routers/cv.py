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
    # 1. Download the PDF from Drive into a temp file
    local_pdf = temp_file_path(suffix=".pdf")
    drive.download_from_drive(drive_link, local_pdf)

    # 2. Parse text from PDF
    raw_text = parser.parse_text(local_pdf)
    
    # 3. Extract structured data
    structured_data = llm.extract_structured_data(raw_text)

    # 4. Generate LaTeX and compile
    tex_content = templater.render_latex(structured_data)
    pdf_path = compiler.compile_pdf(tex_content)

    # 5. Re-upload or return existing link
    new_drive_url = drive.upload_to_drive(pdf_path)
    random_id = str(uuid.uuid4())
    db.set(f"{random_id}",{
        "drive_url": new_drive_url,
        "status": "pending",
    }),

    
    response.status_code = 202
    return {"success": True, "status": "pending"}

@router.get("/status/{cv_id}")
def get_status(response: Response, cv_id: str):
    """
    Fetches the status of a job using its ID.
    """
    cur_cv = db.get(cv_id)
    if not cur_cv:
        response.status_code = 404
        return {"error": "CV ID not found."}
    if cur_cv["status"] == "processing":
        response.status_code = 202
        return {"success": True, "status": "processing"}
    elif cur_cv["status"] == "Done":
        response.status_code = 200
        return {"success": True, "drive_url": cur_cv["drive_url"]}
    
    response.status_code = 500
    return {"error": "Unexpected status value."}

