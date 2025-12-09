# app/schemas/auth_schemas.py
from pydantic import BaseModel, EmailStr

class SignupSchema(BaseModel):
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    public_code: str
