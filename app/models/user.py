# app/models/user.py
from bson import ObjectId

def serialize_user(data):
    return {
        "id": str(data["_id"]),
        "email": data["email"],
        "password": data["password"],
        "public_code": data["public_code"],
    }
