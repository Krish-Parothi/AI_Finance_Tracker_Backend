# dependency
from fastapi import Header, HTTPException, Request
from app.utils.jwt_handler import decode_token

# async def auth_user(authorization: str = Header(None)):
#     if not authorization:
#         raise HTTPException(401)
#     token = authorization.split(" ")[1]
#     payload = decode_token(token)
#     return payload["user_id"]

async def auth_user(req: Request):
    token = req.cookies.get("access_token")
    if not token:
        raise HTTPException(401, "Not authenticated")
    payload = decode_token(token)
    return payload["user_id"]