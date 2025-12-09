# app/schemas/expense_schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    timestamp: datetime
    source: Optional[str] = None
    metadata: Optional[dict] = None

class DateRange(BaseModel):
    start: datetime
    end: datetime
