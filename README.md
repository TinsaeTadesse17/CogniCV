# 💼 CVForge - Kifiya Internal CV Standardization Tool

> **Standardize. Extract. Empower.**  
> CVForge is an internal tool for Kifiya to convert employee CVs into a unified LaTeX-based format and extract key information using AI.

---

## 📝 Table of Contents

1.  [Overview](#overview)
2.  [Features](#features)
3.  [How it Works](#how-it-works)
4.  [Tech Stack](#tech-stack)
5.  [Project Structure](#project-structure)
6.  [Prerequisites](#prerequisites)
7.  [Setup and Installation](#setup-and-installation)
8.  [Running the Application](#running-the-application)
9.  [API Endpoints](#api-endpoints)
10. [Configuration](#configuration)

---

## 📦 Overview

CVForge is designed to streamline the processing of Curriculum Vitae (CVs) within Kifiya. It takes CVs, typically in PDF format from Google Drive links or as a batch upload via a CSV file, and performs the following key operations:

1.  **Downloads** the CV from the provided Google Drive link.
2.  **Parses** the text content from the PDF.
3.  **Extracts** structured information (personal details, education, experience, skills, etc.) using a Large Language Model (LLM - Google Gemini).
4.  **Generates** a new CV in a standardized LaTeX format based on the extracted data.
5.  **Compiles** the LaTeX document into a PDF.
6.  **Uploads** the newly generated, standardized PDF back to Google Drive and provides a shareable link.

This process ensures that all employee CVs adhere to a consistent format, making them easier to manage, review, and utilize for internal purposes.

---

## ⚙️ Features

-   **Single CV Processing**: Upload a Google Drive link to a PDF CV for individual processing.
-   **Batch CV Processing**: Upload a CSV file containing multiple Google Drive links for batch processing.
-   **Automated LaTeX Conversion**: Converts extracted CV data into a predefined, professional LaTeX template.
-   **LLM-Powered Data Extraction**: Utilizes Google Gemini (via Langchain) to parse raw CV text and extract structured data according to a Pydantic schema.
-   **Standardized PDF Output**: Generates clean, uniformly formatted PDF CVs.
-   **Google Drive Integration**: Seamlessly downloads source CVs and uploads processed CVs to Google Drive.
-   **Web Interface**: A Next.js frontend provides an easy-to-use interface for uploading CVs and viewing results.
-   **Background Task Processing**: Batch CSV uploads are handled in the background to prevent UI blocking.
-   **Status Tracking**: API endpoints to check the status of individual CV processing or batch jobs.
-   **Dockerized LaTeX Compilation**: Ensures consistent LaTeX compilation environment using Docker.

---

## 🛠️ How it Works

The process flow is as follows:

1.  **Upload**:
    *   **Single CV**: User provides a Google Drive link to a PDF CV via the web interface.
    *   **Batch CVs**: User uploads a CSV file where each row contains a `cv_link` (Google Drive link to a PDF CV).
2.  **Backend Processing (FastAPI)**:
    *   The backend receives the request.
    *   **Download**: The CV PDF is downloaded from Google Drive.
    *   **Parse**: Text is extracted from the PDF using PyMuPDF.
    *   **Extract**: The raw text is sent to a Google Gemini model (via Langchain) to extract structured information based on a predefined `CVSchema`.
    *   **Template**: The structured data is used to populate a LaTeX template.
    *   **Compile**: The LaTeX string is compiled into a PDF using `pdflatex` running in a Docker container. This happens in two passes to ensure cross-references are correct.
    *   **Upload**: The generated PDF is uploaded back to Google Drive, and its permissions are set to publicly readable.
3.  **Response**:
    *   **Single CV**: A direct link to the processed CV on Google Drive is returned.
    *   **Batch CVs**: A job ID is returned. The frontend polls a status endpoint. Once processing is complete, a link to a new CSV file (containing original data + links to processed CVs) on Google Drive is provided.
4.  **Notification**: For batch CSV processing, the user is notified (sound and browser notification if permission granted) when the job is complete.

---

## 💻 Tech Stack

-   **Backend**:
    *   Python 3
    *   FastAPI (Web framework)
    *   Pydantic (Data validation and settings management)
    *   Langchain (LLM integration)
    *   Google Generative AI (for Gemini LLM)
    *   PyMuPDF (PDF text extraction)
    *   Google API Client Library for Python (Google Drive integration)
    *   Uvicorn (ASGI server)
-   **Frontend**:
    *   Next.js (React framework)
    *   TypeScript
    *   Tailwind CSS (Styling)
    *   React Dropzone (File uploads)
-   **LaTeX Compilation**:
    *   Docker
    *   `pdflatex` (via `kjarosh/latex:2025.1` Docker image)
-   **Database/Storage**:
    *   In-memory Python dictionary (for job status tracking - suitable for single-instance deployment)
    *   Google Drive (for storing original and processed CVs)
-   **Development & Build**:
    *   `Makefile` for build and run commands
    *   `docker-compose` for managing the LaTeX compilation service

---

## 📂 Project Structure

```
.
├── credentials.json        # Google Cloud service account key (GITIGNORED)
├── docker-compose.yml      # Docker Compose for LaTeX service
├── Dockerfile.tex          # Dockerfile for LaTeX environment
├── frontend/               # Next.js frontend application
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── ...
├── Makefile                # Make commands for build, run, clean
├── README.md               # This file
├── requirements.txt        # Python backend dependencies
├── src/                    # FastAPI backend application
│   ├── core/               # Configuration (e.g., API keys)
│   ├── main.py             # FastAPI app entry point
│   ├── models/             # Pydantic models (DTOs, schemas)
```

---

## ✅ Prerequisites

-   **Python 3.10+** and `pip`
-   **Node.js and npm/yarn/pnpm** (for the frontend)
-   **Docker and Docker Compose** (for LaTeX compilation)
-   **Google Cloud Project**:
    *   A Google Cloud Platform (GCP) project is required.
    *   **Enable Google Drive API**: Within your GCP project, you need to enable the Google Drive API. You can find instructions on how to enable APIs [here](https://cloud.google.com/apis/docs/getting-started#enabling_apis).
    *   **Create a Service Account**: Create a service account with appropriate permissions to access Google Drive (e.g., roles that allow reading and writing files if the service account will be uploading/downloading).
        *   Follow the guide for creating a service account [here](https://cloud.google.com/iam/docs/service-accounts-create).
    *   **Download Service Account Key**: After creating the service account, generate a JSON key and download it. Rename this file to `credentials.json` and place it in the project root. This file is sensitive and should not be committed to version control.
-   **Gemini API Key**:
    *   You need an API key for Google Gemini (Generative Language API).
    *   You can obtain an API key by following the instructions on the Google AI for Developers website. Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to create and manage your API keys.

---

## 🚀 Setup and Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Kifiya-Agentic-HR/CVForge
    cd CVForge
    ```

2.  **Set up Google Credentials**:
    *   Place your downloaded Google Cloud service account key file (renamed to `credentials.json`) in the project root directory.
    *   This file is listed in `.gitignore` and should **never** be committed to the repository.

3.  **Configure Environment Variables**:
    *   Place your downloaded Google Cloud service account key file (renamed to `credentials.json`) in the project root directory.
    *   This file is listed in `.gitignore` and should **never** be committed to the repository.

3.  **Configure Environment Variables**:
    *   The project uses an `.env.example` file as a template for environment variables. Copy it to create your own `.env` file:
        ```bash
        cp .env.example .env
        ```
    *   Open the `.env` file and fill in the required values:
        ```env
        GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
        GOOGLE_CLOUD_PROJECT=<your-gcp-project-id> # Replace with your actual Google Cloud Project ID
        GEMINI_API_KEY=<your-gemini-api-key> # Replace with your Google Gemini API Key
        ```
        *   `GOOGLE_APPLICATION_CREDENTIALS`: Should already be set to `./credentials.json` if you followed the step above.
        *   `GOOGLE_CLOUD_PROJECT`: Enter the Project ID of your Google Cloud Project where you enabled the Drive API and created the service account.
        *   `GEMINI_API_KEY`: Enter the API key you obtained for the Gemini API.

4.  **Build the project**:
    ```bash
    make build
    ```
5.  **Run the project**:
    ```bash
    make run
    ```
6.  **Access the application**:
    *   The backend will be available at `http://localhost:8000`.
    *   The frontend will be available at `http://localhost:3000`.

---