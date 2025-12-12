# app/routers/expenses.py
from fastapi import APIRouter, Depends
from app.db import expenses, oid
from app.schemas.expense_schemas import ExpenseCreate, DateRange
from app.utils.responses import success
from app.middleware.error_handler import register_exception_handlers
from datetime import datetime
# from .auth import auth_user
from app.utils.auth_dependency import auth_user
from app.models.expense import serialize_expense

router = APIRouter()

@router.post("/add")
def add_expense(data: ExpenseCreate, user_id: str = Depends(auth_user)):
    payload = {
        "user_id": oid(user_id),
        "amount": data.amount,
        "category": data.category,
        "description": data.description,
        "timestamp": data.timestamp.isoformat(),
        "source": data.source,
        "metadata": data.metadata or {},
        "created_at": datetime.utcnow().isoformat(),
    }
    expenses.insert_one(payload)
    return success("expense_added")

@router.get("/list")
def list_expenses(user_id: str = Depends(auth_user)):
    docs = expenses.find({"user_id": oid(user_id)})
    return success("ok", [d for d in docs])

@router.post("/range")
def expense_range(r: DateRange, user_id: str = Depends(auth_user)):
    q = {
        "user_id": oid(user_id),
        "timestamp": {"$gte": r.start.isoformat(), "$lte": r.end.isoformat()},
    }
    docs = expenses.find(q)
    return success("ok", [serialize_expense(d) for d in docs])
