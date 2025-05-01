import subprocess
import os
import uuid

def compile_pdf(tex_content: str) -> str:
    output_dir = os.path.join("generated_pdfs", str(uuid.uuid4()))
    os.makedirs(output_dir, exist_ok=True)

    tex_file = os.path.join(output_dir, "cv.tex")
    with open(tex_file, "w") as f:
        f.write(tex_content)

    subprocess.run(["latexmk", "-pdf", "cv.tex"], cwd=output_dir, check=True)

    return os.path.join(output_dir, "cv.pdf")
