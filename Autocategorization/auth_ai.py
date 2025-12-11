# app/routers/llm.py
from fastapi import APIRouter, Response, Depends, HTTPException, Request
from pydantic import BaseModel
import jwt, os
from datetime import datetime, timedelta
from Autocategorization.llm import LLMExtractor
from Autocategorization.db import DBWriter
from app.utils.auth_dependency import auth_user
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
SECRET = os.getenv("JWT_SECRET")
extractor = LLMExtractor()
writer = DBWriter()


class LoginReq(BaseModel):
    username: str
    password: str


class ParagraphReq(BaseModel):
    paragraph: str


def create_token(data, minutes=60):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=minutes)
    return jwt.encode(payload, SECRET, algorithm="HS256")


def get_current_user(req: Request):
    token = req.cookies.get("access_token")
    if not token:
        raise HTTPException(401, "Not authenticated")
    try:
        return jwt.decode(token, SECRET, algorithms=[os.getenv("JWT_ALGORITHM")])
    except:
        raise HTTPException(401, "Invalid token")


@router.post("/login")
def login(req: LoginReq, response: Response):
    if req.username != "user" or req.password != "pass":
        raise HTTPException(401, "Invalid credentials")
    user = {"user_id": "user123", "username": req.username}
    token = create_token(user)
    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return {"status": "logged in", "user_id": user["user_id"]}


@router.post("/auto-categorize")
def auto_categorize(data: ParagraphReq, request: Request, user=Depends(auth_user)):
    # Ensure there is some input
    if not data.paragraph or data.paragraph.strip() == "":
        raise HTTPException(400, "No text input provided for extraction")
    
    # Extract expenses
    expenses = extractor.extract(data.paragraph)
    
    # Only insert if extraction produced valid entries
    if not expenses:
        return {"inserted": 0, "parsed": []}
    
    count = writer.insert_expenses(user_id=user, expenses=expenses)
    return {"inserted": count, "parsed": expenses}
