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
You receive only the user's expense JSON. Use only this data.
Never assume identity or personal details.
Answer the question strictly based on the expenses.

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
