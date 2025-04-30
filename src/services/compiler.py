import subprocess
import os
import uuid

def compile_pdf(tex_content: str) -> str:
    temp_dir = f"/tmp/{uuid.uuid4()}"
    os.makedirs(temp_dir, exist_ok=True)
    tex_file = os.path.join(temp_dir, "cv.tex")
    with open(tex_file, "w") as f:
        f.write(tex_content)

    subprocess.run(["latexmk", "-pdf", "cv.tex"], cwd=temp_dir, check=True)

    return os.path.join(temp_dir, "cv.pdf")
