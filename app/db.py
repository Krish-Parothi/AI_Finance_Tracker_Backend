# app/db.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING
from bson import ObjectId

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

users = db["users"]
expenses = db["expenses"]

users.create_index([("email", ASCENDING)], unique=True)
expenses.create_index([("user_id", ASCENDING)])
expenses.create_index([("timestamp", ASCENDING)])

def oid(id_str):
    return ObjectId(id_str)
