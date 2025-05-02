from src.models.dtos import CVSchema
from langchain import PromptTemplate, LLMChain
from langchain_google_vertexai import ChatVertexAI

# --- Corrected Function ---
def extract_structured_data(raw_text: str) -> CVSchema:
    """
    Extracts structured data from raw CV text directly into the CVSchema format.
    """
    llm = ChatVertexAI(
        model_name="gemini-pro",
        temperature=0.0,
        max_output_tokens=4096,
    )
    model_with_schema = llm.with_structured_output(CVSchema)

    prompt = PromptTemplate(
        input_variables=["raw_text"],
        template="""
Extract information from the CV text below and format it strictly according to the following Pydantic schema structure.
Output EXACTLY the JSON matching this schema. Be thorough and extract all relevant details. If a field is optional and not found, omit it or set it to null.

SCHEMA:
{{
    "personal_info": {{
        "full_name": "string (required)",
        "location": "string (optional)",
        "email": "string (email format, optional)",
        "phone": "string (optional)",
        "website": "string (URL format, optional)",
        "linkedin": "string (URL format, optional)",
        "github": "string (URL format, optional)"
    }},
    "summary": {{
        "text": "string (required, the professional summary)"
    }} (optional section),
    "education": [
        {{
            "institution": "string (required)",
            "degree": "string (optional)",
            "field_of_study": "string (optional)",
            "start_date": "string (e.g., 'YYYY-MM' or 'YYYY', optional)",
            "end_date": "string (e.g., 'YYYY-MM', 'YYYY', or 'Present', optional)",
            "location": "string (optional)",
            "gpa": "string (optional)",
            "coursework": ["string", ...] (optional)
        }},
        ...
    ] (optional section),
    "experience": [
        {{
            "company": "string (required)",
            "role": "string (required, job title)",
            "start_date": "string (e.g., 'YYYY-MM' or 'YYYY', optional)",
            "end_date": "string (e.g., 'YYYY-MM', 'YYYY', or 'Present', optional)",
            "location": "string (optional)",
            "achievements": ["string (bullet points describing responsibilities/accomplishments)", ...] (optional)
        }},
        ...
    ] (optional section),
    "publications": [
         {{
            "title": "string (required)",
            "authors": ["string", ...] (optional)",
            "date": "string (e.g. 'YYYY-MM', optional)",
            "publisher": "string (optional)",
            "doi": "string (optional)",
            "url": "string (URL format, optional)"
        }},
        ...
    ] (optional section),
    "projects": [
        {{
            "name": "string (required)",
            "description": "string (optional)",
            "url": "string (URL format, optional)",
            "start_date": "string (optional)",
            "end_date": "string (optional)",
            "tools_used": ["string", ...] (optional)",
            "highlights": ["string", ...] (optional)"
        }},
        ...
    ] (optional section),
    "skills": {{
        "programming_languages": ["string", ...] (optional),
        "frameworks_libraries": ["string", ...] (optional),
        "tools": ["string", ...] (optional),
        "other": ["string", ...] (optional)
    }} (optional section)
}}

CV TEXT:
{raw_text}
""".strip(),
    )

    # 3) Build & run chain
    chain = LLMChain(
        llm=model_with_schema,
        prompt=prompt,
        output_key="parsed_cv" # Renamed output key for clarity
    )

    result = chain.invoke({"raw_text": raw_text})
    parsed: CVSchema = result["parsed_cv"]
    return parsed
