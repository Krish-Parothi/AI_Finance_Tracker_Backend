# app/routers/analytics.py
from fastapi import APIRouter, Depends
from app.db import expenses, oid
from app.utils.responses import success
from datetime import datetime, timedelta
# from auth import auth_user
from app.utils.auth_dependency import auth_user

router = APIRouter()

@router.get("/week")
def last_week(user_id: str = Depends(auth_user)):
    end = datetime.utcnow()
    start = end - timedelta(days=7)
    docs = expenses.find({
        "user_id": oid(user_id),
        "timestamp": {"$gte": start.isoformat(), "$lte": end.isoformat()},
    })
    return success("ok", [d for d in docs])
