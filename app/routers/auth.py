# app/routers/auth.py
from fastapi import APIRouter, Depends, Response
from app.schemas.auth_schemas import SignupSchema, LoginSchema, TokenOut
from app.db import users
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_handler import create_access_token, create_refresh_token
from app.utils.responses import success, error
from bson import ObjectId
from app.utils.auth_dependency import auth_user
from app.db import users, oid

router = APIRouter()

def generate_public_code():
    count = users.count_documents({})
    return f"USER{str(count+1).zfill(3)}"

@router.post("/signup")
def signup(data: SignupSchema):
    if users.find_one({"email": data.email}):
        return error("email_exists")
    hashed = hash_password(data.password)
    public_code = generate_public_code()
    doc = {
        "email": data.email,
        "password": hashed,
        "public_code": public_code,
    }
    inserted = users.insert_one(doc)
    return success("signup_ok", {"user_id": str(inserted.inserted_id)})

@router.post("/login", response_model=TokenOut)
def login(data: LoginSchema, response: Response):
    user = users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        return error("invalid_credentials")
    
    uid = str(user["_id"])
    access_token = create_access_token(uid)
    refresh_token = create_refresh_token(uid)
    
    # Set HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # True if HTTPS
        samesite="lax"
    )
    
    return {
        "user_id": uid,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "public_code": user["public_code"],
    }

@router.get("/me")
def me(user_id: str = Depends(auth_user)):
    _id = oid(user_id)

    doc = users.find_one({"_id": _id})
    if not doc:
        return {"success": False, "message": "user_not_found"}

    return {
        "success": True,
        "data": {
            "id": str(doc["_id"]),
            "username": doc.get("username"),
            "email": doc.get("email"),
        }
    }
