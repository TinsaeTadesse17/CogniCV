import subprocess
import tempfile
import shutil
import logging
import uuid
from pathlib import Path
import os

from src.models.dtos import CVSchema
from src.services.templater import generate_cv_latex

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

# Determine Project Root dynamically
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "generated_pdfs"
DOCKER_SERVICE_NAME = "latex_compiler"
LATEX_COMPILER = "pdflatex"

DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# --- End Configuration ---

class LatexCompilationError(Exception):
    """Custom exception for LaTeX compilation failures."""
    def __init__(self, message, stdout=None, stderr=None, log_content=None):
        super().__init__(message)
        self.stdout = stdout
        self.stderr = stderr
        self.log_content = log_content

def compile_latex_string_to_pdf(
    cv_schema: CVSchema,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    output_filename_base: str = "cv_output"
) -> Path:
    
    if not isinstance(cv_schema, CVSchema):
        raise TypeError("cv_schema must be an instance of CVSchema.")
    
    latex_string = generate_cv_latex(cv_schema)

    if not latex_string:
        raise ValueError("Input LaTeX string cannot be empty.")

    output_dir.mkdir(parents=True, exist_ok=True)

    temp_dir_name = f"latex_temp_{uuid.uuid4()}"
    temp_dir_host_path = PROJECT_ROOT / temp_dir_name
    temp_dir_host_path.mkdir()
    log.info(f"Created temporary directory on host: {temp_dir_host_path}")

    temp_base_name = f"doc_{uuid.uuid4()}"
    temp_tex_file_host = temp_dir_host_path / f"{temp_base_name}.tex"
    temp_pdf_file_host = temp_dir_host_path / f"{temp_base_name}.pdf"
    temp_log_file_host = temp_dir_host_path / f"{temp_base_name}.log"

    try:
        log.info(f"Writing LaTeX string to temporary file: {temp_tex_file_host}")
        with open(temp_tex_file_host, "w", encoding="utf-8") as f:
            f.write(latex_string)

        temp_dir_container = Path("/app") / temp_dir_host_path.name
        temp_tex_file_container = temp_dir_container / temp_tex_file_host.name

        for run in range(1, 3):
            log.info(f"Starting Docker LaTeX compilation via service '{DOCKER_SERVICE_NAME}' (Pass {run}/2)...")
            cmd = [
                "docker", "compose", "run", "--rm",
                DOCKER_SERVICE_NAME,
                LATEX_COMPILER,
                "-interaction=nonstopmode",
                f"-output-directory={temp_dir_container}",
                str(temp_tex_file_container)
            ]
            log.debug(f"Executing command: {' '.join(map(str, cmd))}")

            process = subprocess.run(
                cmd,
                capture_output=True, text=True, encoding='utf-8',
                cwd=PROJECT_ROOT, check=False
            )

            if process.returncode != 0:
                log.error(f"Docker LaTeX compilation failed (Pass {run})!")
                log_content = None
                if temp_log_file_host.exists():
                    try:
                        with open(temp_log_file_host, "r", encoding='utf-8', errors='ignore') as logf:
                            log_content = logf.read()
                            log.debug(f"Log content from {temp_log_file_host}:\n{log_content}")
                    except Exception as log_read_err:
                        log.warning(f"Could not read log file {temp_log_file_host}: {log_read_err}")
                raise LatexCompilationError(
                    f"LaTeX compilation failed on pass {run}.",
                    stdout=process.stdout, stderr=process.stderr, log_content=log_content
                )
            log.info(f"Docker LaTeX compilation (Pass {run}/2) successful.")

        if not temp_pdf_file_host.exists():
            raise RuntimeError(f"PDF file not found at {temp_pdf_file_host} after successful compilation steps.")

        final_pdf_filename = f"{output_filename_base}_{uuid.uuid4()}.pdf"
        final_pdf_path = output_dir / final_pdf_filename
        final_pdf_path = final_pdf_path.resolve()

        log.info(f"Moving compiled PDF from {temp_pdf_file_host} to {final_pdf_path}")
        shutil.move(str(temp_pdf_file_host), str(final_pdf_path))

        log.info(f"Successfully generated PDF: {final_pdf_path}")
        return final_pdf_path

    except FileNotFoundError as e:
        log.exception(f"Error running subprocess - 'docker' command not found? {e}")
        raise FileNotFoundError("Docker command not found. Ensure Docker is installed and accessible.") from e
    except LatexCompilationError as e:
        log.error("--- LaTeX Compilation Failure Details ---")
        log.error(f"Error Message: {e}")
        raise e
    except Exception as e:
        log.exception(f"An unexpected error occurred during PDF compilation: {e}")
        raise RuntimeError(f"An unexpected error occurred: {e}") from e
    finally:
        if temp_dir_host_path.exists():
            log.info(f"Cleaning up temporary directory: {temp_dir_host_path}")
            try:
                shutil.rmtree(temp_dir_host_path)
            except OSError as e:
                log.error(f"Failed to remove temporary directory {temp_dir_host_path}: {e}")
