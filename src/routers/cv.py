from fastapi import APIRouter, UploadFile, File
from src.services import parser, llm, templater, compiler, drive
from src.utils import file_ops

router = APIRouter()

@router.post("/upload")
async def upload_cv(file: UploadFile = File(...)):
    # Save uploaded file
    file_path = file_ops.save_temp_file(file)

    # Parse text from PDF
    raw_text = parser.parse_text(file_path)

    # Extract structured data using LLM
    structured_data = llm.extract_structured_data(raw_text)

    # Generate LaTeX content
    tex_content = templater.render_latex(structured_data)

    # Compile LaTeX to PDF
    pdf_path = compiler.compile_pdf(tex_content)

    # Upload PDF to Google Drive
    drive_url = drive.upload_to_drive(pdf_path)

    return {"drive_url": drive_url}
