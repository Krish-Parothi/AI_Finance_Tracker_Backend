# whatsapp_user_service.py
from Whatsapp_Integration.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

users = db["users"]

def signup_user(phone: str, username: str, password: str):
    if users.find_one({"phone": phone}):
        return None  # Already exists
    hashed_pw = generate_password_hash(password)
    user_doc = {
        "phone": phone,
        "username": username,
        "password": hashed_pw,
        "public_code": f"USER{int(datetime.utcnow().timestamp())}",
        "created_at": datetime.utcnow().isoformat()
    }
    users.insert_one(user_doc)
    return user_doc

def login_user(phone: str, password: str):
    user = users.find_one({"phone": phone})
    if not user or not check_password_hash(user["password"], password):
        return None
    return user
