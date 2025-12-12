# dependency
from fastapi import Header, HTTPException, Request
from app.utils.jwt_handler import decode_token

# async def auth_user(authorization: str = Header(None)):
#     if not authorization:
#         raise HTTPException(401)
#     token = authorization.split(" ")[1]
#     payload = decode_token(token)
#     return payload["user_id"]

# async def auth_user(req: Request):
#     token = req.cookies.get("access_token")
#     if not token:
#         raise HTTPException(401, "Not authenticated")
#     payload = decode_token(token)
#     return payload["user_id"]

# async def auth_user(authorization: str = Header(None)):
#     if not authorization:
#         raise HTTPException(401, "No authorization header")

#     token = authorization.split(" ")[1]
#     payload = decode_token(token)
#     return payload["user_id"]

async def auth_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Authorization header missing")

    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(401, "Invalid token scheme")

        payload = decode_token(token)
        return payload["user_id"]

    except Exception as e:
        raise HTTPException(401, "Invalid or expired token")