# 💼 CVForge

> **Standardize. Extract. Empower.**  
> Convert any CV upload into a unified LaTeX layout and extract key entities via LLM.

---

## 🔍 Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Architecture](#architecture)  

---

## 📦 Overview

CVForge is a toolkit for:

- **Uploading** PDF/DOCX resumes via a web form  
- **Converting** them into a consistent, publication-quality LaTeX template  

This enables HR systems, applicant-tracking systems, or analytics pipelines to consume CV data in a reliable, standardized way.

---

## ⚙️ Features

- **Automated LaTeX conversion** with custom templates  
- **LLM-powered NER** for robust, AI-driven entity extraction  
- **JSON output** with a unified schema for easy downstream integration  
- **Extensible plugin system** for adding new templates or extraction rules  

---

## 🏗 Architecture

```text
[Web Client] ──> [Backend API]
                       ├─> Storage (e.g., S3)
                       ├─> LaTeX Converter Service
                       └─> LLM Extraction Service
                             └─> Outputs JSON → Database / API consumer
Frontend: React or Vue form uploads resumes to the backend.

API: FastAPI (Python) handles file storage, queueing, and orchestration.

LaTeX Service: Converts files through Pandoc + custom .tex templates.

Extraction Service: Calls out to an LLM (e.g., OpenAI) for entity recognition, then normalizes into your schema.

Persistence: Stores JSON outputs in Postgres or MongoDB for retrieval.
```

