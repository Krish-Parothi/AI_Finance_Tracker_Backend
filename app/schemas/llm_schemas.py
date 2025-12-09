# app/schemas/llm_schemas.py
from pydantic import BaseModel

class LLMQuery(BaseModel):
    query: str
