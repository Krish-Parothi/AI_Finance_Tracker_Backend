# app/middleware/error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.responses import error

def register_exception_handlers(app):
    @app.exception_handler(Exception)
    async def handler(request: Request, exc: Exception):
        return JSONResponse(status_code=400, content=error(str(exc)))
