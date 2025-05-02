import os
import uuid
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from src.utils.inmemory import db

def compile_pdf(cv_id : str,text: str) -> str:
    output_dir = os.path.join("generated_pdfs", str(uuid.uuid4()))
    os.makedirs(output_dir, exist_ok=True)

    pdf_path = os.path.join(output_dir, "cv.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    
    width, height = A4
    margin = 50
    y = height - margin

    for line in text.splitlines():
        if y < margin:
            c.showPage()
            y = height - margin
        c.drawString(margin, y, line)
        y -= 15

    c.save()
    if not os.path.exists(pdf_path):
        db.set(f"{cv_id}",{
            "status": "failed",
        }),
        raise Exception("PDF generation failed.")
        
    return pdf_path
