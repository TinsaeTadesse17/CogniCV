from src.models.dtos import CVSchema
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# --- Corrected Function ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
# Removed the erroneous import
from src.models.dtos import CVSchema
import json

def extract_structured_data(raw_text: str) -> CVSchema:
    # 1) Initialize and wrap LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        # temperature=0.0,
        max_output_tokens=4096,
    )
    model_with_schema = llm.with_structured_output(CVSchema)

    # 2) Build prompt (inject the JSON schema automatically for clarity)
    schema_json = json.dumps(CVSchema.model_json_schema(), indent=2)
    prompt = PromptTemplate(
        input_variables=["raw_text", "schema_json"],
        template="""
Extract information from the CV text below and format it strictly according to the json schema.
Output exactly the JSON matching this schema without any '```' json or any text. You should account the nested json structure as well.

CV TEXT:
{raw_text}

OUTPUT JSON SCHEMA:
{schema_json}
""".strip(),
    )

    # 3) Compose chain and invoke using LLMChain
    chain = prompt | model_with_schema
    input_data = {
        "raw_text": raw_text,
        "schema_json": schema_json,
    }
    parsed: CVSchema = chain.invoke(input=input_data)

    return parsed
