from pymongo import MongoClient
from datetime import datetime
import os
MONGO_URI = os.getenv("MONGO_URI")

class DBWriter:
    def __init__(self):
        self.collection = MongoClient(MONGO_URI)["finance_db"]["expenses"]

    def insert_expenses(self, user_id: str, expenses: list):
        if not expenses: return 0
        docs = [{"user_id": user_id, **e, "created_at": datetime.utcnow()} for e in expenses]
        self.collection.insert_many(docs)
        return len(docs)
