from fastapi import FastAPI
from whatsapp_webhook import router as text_expense_router

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"status": "ok"}


app.include_router(text_expense_router, prefix="/api/whatsapp")
#main.py

