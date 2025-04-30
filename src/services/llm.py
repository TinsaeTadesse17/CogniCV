from langchain_google_vertexai import ChatVertexAI
from langchain_core.pydantic_v1 import BaseModel as LCBaseModel
from langchain import PromptTemplate, LLMChain
from src.core.models.dtos import CVSchema

class CVOutput(CVSchema, LCBaseModel):
    """LangChain wrapper to parse structured CV output."""

def extract_structured_data(raw_text: str) -> CVSchema:
    # 1. Initialize Gemini via Vertex AI
    llm = ChatVertexAI(
        model_name="gemini-pro",       # or "gemini-1.5-pro", "gemini-2.0-flash-exp", etc.
        temperature=0.0,               # deterministic output for structured parsing
        max_output_tokens=1024,        # adjust as needed
    )
    # 2. Enforce our Pydantic schema on the LLM’s output
    model_with_schema = llm.with_structured_output(CVOutput)

    # 3. Define the prompt
    template = PromptTemplate(
        input_variables=["raw_text"],
        template="""
Extract the following fields from the CV text below and output as JSON conforming exactly to the CVOutput schema:
{{
  "contact": {{ name, email, phone, website }},
  "summary": {{ summary }},
  "experience": [{{ company, title, start_date, end_date, responsibilities }}...],
  "education": [{{ institution, degree, start_year, end_year }}...],
  "skills": [string...]
}}
-----
CV TEXT:
{raw_text}
""".strip()
    )

    # 4. Build the chain
    cv_chain = LLMChain(
        llm=model_with_schema,
        prompt=template,
        output_key="cv_structured"
    )

    # 5. Run and return our typed CVSchema
    result: CVOutput = cv_chain.run_and_return_object(raw_text=raw_text)
    return result
