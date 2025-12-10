# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.error_handler import register_exception_handlers
from app.routers import auth, expenses, analytics, llm
from Autocategorization import auth_ai
from Whatsapp_Integration.whatsapp_webhook import router as text_expense_router
from Image_Vision.router import router as vision_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(llm.router, prefix="/llm", tags=["llm"])
app.include_router(auth_ai.router, prefix="/api", tags=["auth-ai"])
app.include_router(text_expense_router, prefix="/api/whatsapp")
app.include_router(vision_router, prefix="/api/vision", tags=["vision"])