# app/models/expense.py
def serialize_expense(data):
    return {
        "id": str(data["_id"]),
        "user_id": str(data["user_id"]),
        "amount": data["amount"],
        "category": data["category"],
        "description": data["description"],
        "timestamp": data["timestamp"],
        "source": data["source"],
        "metadata": data["metadata"],
        "created_at": data["created_at"],
    }
