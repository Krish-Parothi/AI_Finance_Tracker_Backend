from fastapi import APIRouter, UploadFile, File, Depends
from datetime import datetime
from Image_Vision.vision import parse_bill
from app.utils.auth_dependency import auth_user
from app.db import expenses

router = APIRouter()

@router.post("/upload-bill")
async def upload_bill(file: UploadFile = File(...), user_id: str = Depends(auth_user)):
    """
    Upload a bill image, parse it using vision LLM, auto-categorize expenses,
    and insert into MongoDB.
    """
    # Read image bytes
    image_bytes = await file.read()

    # Parse with vision LLM
    parsed_expenses = parse_bill(image_bytes)

    # Insert parsed expenses into MongoDB
    for item in parsed_expenses:
        expenses.insert_one({
            "user_id": user_id,
            "description": item.get("description", ""),
            "amount": float(item.get("amount", 0)),
            "category": item.get("category", "Other"),
            "timestamp": item.get("timestamp") or datetime.utcnow().isoformat(),
            "source": "web-image",
            "metadata": item.get("metadata", {}),
            "created_at": datetime.utcnow().isoformat()
        })

    return {"status": "success", "count of items": len(parsed_expenses), "Operation": "Expense Added Successfully."}
