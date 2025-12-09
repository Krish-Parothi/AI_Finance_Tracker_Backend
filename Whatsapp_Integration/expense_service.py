# expense_service.py
from datetime import datetime
from Whatsapp_Integration.db import db

expenses = db["expenses"]

def add_expense(user_id: str, expense_data: dict):
    expense_record = {
        "user_id": user_id,  # link to registered user
        "amount": expense_data.get("amount"),
        "category": expense_data.get("category"),
        "description": expense_data.get("description"),
        "timestamp": expense_data.get("timestamp", datetime.utcnow().isoformat()),
        "source": "whatsapp",
        "metadata": expense_data.get("metadata", {}),
        "created_at": datetime.utcnow().isoformat()
    }
    result = expenses.insert_one(expense_record)
    return str(result.inserted_id)
