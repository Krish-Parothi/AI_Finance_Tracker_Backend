# from fastapi import APIRouter, Depends, HTTPException
# from datetime import datetime, timedelta
# from app.utils.auth_dependency import auth_user
# from app.db import db
# from app.db import oid

# router = APIRouter()
# transactions = db["expenses"]

# @router.get("/summary")
# def dashboard_summary(user_id: str = Depends(auth_user)):
#     # user_id = ["user_id"]

#     now = datetime.utcnow()
#     current_month_start = datetime(now.year, now.month, 1)
#     last_month_end = current_month_start - timedelta(days=1)
#     last_month_start = datetime(last_month_end.year, last_month_end.month, 1)

#     # txs = list(transactions.find({"user_id": oid(user_id)}))
#     txs_raw = list(transactions.find({"user_id": oid(user_id)}))

#     txs = []
#     for t in txs_raw:
#         ts = t.get("timestamp")
#         if isinstance(ts, str):
#             try:
#                 t["timestamp"] = datetime.fromisoformat(ts)
#             except:
#                 t["timestamp"] = None
#         txs.append(t)

#     total_balance = sum(t.get("amount", 0) for t in txs)

#     monthly_spending = sum(
#         abs(t["amount"]) for t in txs
#         if t["amount"] < 0 and t["timestamp"] >= current_month_start
#     )

#     monthly_income = sum(
#         t["amount"] for t in txs
#         if t["amount"] > 0 and t["timestamp"] >= current_month_start
#     )

#     last_spending = sum(
#         abs(t["amount"]) for t in txs
#         if t["amount"] < 0 and last_month_start <= t["timestamp"] <= last_month_end
#     )

#     last_income = sum(
#         t["amount"] for t in txs
#         if t["amount"] > 0 and last_month_start <= t["timestamp"] <= last_month_end
#     )

#     spending_change = (
#         ((monthly_spending - last_spending) / last_spending) * 100
#         if last_spending > 0 else 0
#     )

#     income_change = (
#         ((monthly_income - last_income) / last_income) / last_income * 100
#         if last_income > 0 else 0
#     )

#     return {
#         "totalBalance": total_balance,
#         "monthlySpending": monthly_spending,
#         "monthlyIncome": monthly_income,
#         "currentBalance": total_balance,
#         "spendingChange": spending_change,
#         "incomeChange": income_change
#     }

from fastapi import APIRouter, Depends
from datetime import datetime, timedelta, timezone
from app.utils.auth_dependency import auth_user
from app.db import db, oid

router = APIRouter()
transactions = db["expenses"]

@router.get("/summary")
def dashboard_summary(user_id: str = Depends(auth_user)):

    now = datetime.now(timezone.utc)
    current_month_start = datetime(now.year, now.month, 1, tzinfo=timezone.utc)

    last_month_end = current_month_start - timedelta(days=1)
    last_month_start = datetime(last_month_end.year, last_month_end.month, 1, tzinfo=timezone.utc)

    txs = list(transactions.find({"user_id": oid(user_id)}))

    # Convert Mongo timestamps to aware datetime
    for t in txs:
        if isinstance(t["timestamp"], str):
            t["timestamp"] = datetime.fromisoformat(t["timestamp"].replace("Z", "+00:00"))

    total_balance = sum(t.get("amount", 0) for t in txs)

    monthly_spending = sum(
        abs(t["amount"]) for t in txs
        if t["amount"] < 0 and t["timestamp"] >= current_month_start
    )

    monthly_income = sum(
        t["amount"] for t in txs
        if t["amount"] > 0 and t["timestamp"] >= current_month_start
    )

    last_spending = sum(
        abs(t["amount"]) for t in txs
        if t["amount"] < 0 and last_month_start <= t["timestamp"] <= last_month_end
    )

    last_income = sum(
        t["amount"] for t in txs
        if t["amount"] > 0 and last_month_start <= t["timestamp"] <= last_month_end
    )

    spending_change = (
        ((monthly_spending - last_spending) / last_spending) * 100
        if last_spending > 0 else 0
    )

    income_change = (
        ((monthly_income - last_income) / last_income) * 100
        if last_income > 0 else 0
    )

    return {
        "totalBalance": total_balance,
        "monthlySpending": monthly_spending,
        "monthlyIncome": monthly_income,
        "currentBalance": total_balance,
        "spendingChange": spending_change,
        "incomeChange": income_change,
    }