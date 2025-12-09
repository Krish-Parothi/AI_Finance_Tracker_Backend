# app/utils/jwt_handler.py
import os
import jwt
from datetime import datetime, timedelta

secret = os.getenv("JWT_SECRET")
algorithm = os.getenv("JWT_ALGORITHM")

def create_access_token(user_id):
    exp = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    return jwt.encode({"user_id": user_id, "exp": exp}, secret, algorithm=algorithm)

def create_refresh_token(user_id):
    exp = datetime.utcnow() + timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")))
    return jwt.encode({"user_id": user_id, "exp": exp}, secret, algorithm=algorithm)

def decode_token(token):
    return jwt.decode(token, secret, algorithms=[algorithm])
