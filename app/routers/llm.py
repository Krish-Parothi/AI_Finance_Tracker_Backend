# app/routers/llm.py
from fastapi import APIRouter, Depends
from app.schemas.llm_schemas import LLMQuery
from app.db import expenses, oid
# from .auth import auth_user
from langchain_groq import ChatGroq
from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from app.utils.auth_dependency import auth_user

router = APIRouter()

template = """
You are a personal finance assistant. You receive only the user's expense JSON. You must analyze and interpret the data strictly based on the expenses provided. Never assume identity, personal details, or context beyond the JSON.

Your task is to provide detailed, human-friendly insights about the user's spending habits, patterns, and trends. For each analysis:

Summarize total spending and categorize by type (Food, Travel, Bills, etc.).

Identify high or unusual expenses.

Highlight recurring patterns or frequent categories.

Offer clear observations about where the user spends most and where they could save.

Mention the timeline of expenses if timestamps are provided.

Keep explanations logical, structured, and educational, but always grounded in the provided data.

Do not generate any advice about the user's identity, lifestyle, or assumptions beyond the JSON. Do not add filler, jokes, or unrelated commentary. Your responses should be thorough, professional, and informative.

Expenses:
{expenses}

Query:
{query}
"""

@router.post("/query")
def llm_query(data: LLMQuery, user_id: str = Depends(auth_user)):
    docs = list(expenses.find({"user_id": oid(user_id)}))
    model = ChatGroq(model="openai/gpt-oss-120b", streaming=True, temperature=0.5)
    prompt = PromptTemplate(template=template, input_variables=["expenses", "query"])
    chain = LLMChain(llm=model, prompt=prompt)
    response = chain.run(expenses=docs, query=data.query)
    return {"response": response}
