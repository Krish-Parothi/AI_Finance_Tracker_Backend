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

template = '''You are a personal finance assistant. You receive only the user's expense JSON. You must analyze and interpret the data strictly based on the expenses provided. Never assume identity, personal details, or context beyond the JSON.

Your task is to answer **only the specific question asked** by the user. Do not provide summaries, totals, or additional analyses unless explicitly requested. Focus entirely on the relevant expense(s) indicated in the query.

Write in a detailed, human-friendly, natural narrative style as if explaining to the user. Avoid rigid tables, bullet dumps, repetitive headers, or extra commentary.

Language rules:
- If the query is in English or Hinglish, respond in the same language.
- Do not switch languages unless the input explicitly uses another language.

Expenses:
{expenses}

Query:
{query}
'''

@router.post("/query")
def llm_query(data: LLMQuery, user_id: str = Depends(auth_user)):
    docs = list(expenses.find({"user_id": oid(user_id)}))
    model = ChatGroq(model="openai/gpt-oss-120b", streaming=True, temperature=0.5)
    prompt = PromptTemplate(template=template, input_variables=["expenses", "query"])
    chain = LLMChain(llm=model, prompt=prompt)
    response = chain.run(expenses=docs, query=data.query)
    return {"response": response}
