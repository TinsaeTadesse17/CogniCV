# src/services/llm.py

from langchain.pydantic_v1 import BaseModel as LCBaseModel, Field
from langchain import PromptTemplate, LLMChain
from langchain_google_vertexai import ChatVertexAI
from src.models.dtos import CVSchema

# 1) LangChain’s shim model—inherits only from LCBaseModel
class CVOutput(LCBaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    phone: str | None = Field(None, description="Phone number")
    website: str | None = Field(None, description="Personal website URL")

    summary: str = Field(..., description="A brief professional summary")

    experience: list[dict] = Field(
        ...,
        description=(
            "List of experience items, each with 'company', 'title', 'start_date', "
            "'end_date', and 'responsibilities' (list of strings)"
        ),
    )

    education: list[dict] = Field(
        ...,
        description=(
            "List of education items, each with 'institution', 'degree', 'start_year', "
            "'end_year'"
        ),
    )

    skills: list[str] = Field(..., description="List of skills")

def extract_structured_data(raw_text: str) -> CVSchema:
    # 2) Instantiate Gemini via Vertex AI
    llm = ChatVertexAI(
        model_name="gemini-pro",
        temperature=0.0,
        max_output_tokens=4000,
    )

    # 3) Enforce our LCBaseModel schema
    model_with_schema = llm.with_structured_output(CVOutput)

    # 4) Prompt definition
    prompt = PromptTemplate(
        input_variables=["raw_text"],
        template="""
Extract fields from the CV text below and output EXACTLY the JSON matching this schema:

- name: string  
- email: string  
- phone: string or null  
- website: string or null  
- summary: string  
- experience: [{{company, title, start_date, end_date, responsibilities}}...]  
- education: [{{institution, degree, start_year, end_year}}...]  
- skills: [string...]

CV TEXT:
{raw_text}
""".strip(),
    )

    # 5) Build & run chain
    chain = LLMChain(
        llm=model_with_schema,
        prompt=prompt,
        output_key="parsed"
    )
    parsed: CVOutput = chain.run_and_return_object(raw_text=raw_text)

    # 6) Convert LCBaseModel → your Pydantic CVSchema
    return CVSchema(
        contact={
            "name": parsed.name,
            "email": parsed.email,
            "phone": parsed.phone,
            "website": parsed.website,
        },
        summary={"summary": parsed.summary},
        experience=[
            item for item in parsed.experience  # already list[dict]
        ],
        education=[
            item for item in parsed.education
        ],
        skills=parsed.skills
    )
