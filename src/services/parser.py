import fitz  # PyMuPDF

def parse_text(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()

    print(f"Extracted text from {file_path}: {text}")  # Print first 100 characters for debugging
    return text
