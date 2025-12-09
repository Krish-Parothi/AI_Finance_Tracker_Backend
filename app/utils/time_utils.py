# app/utils/time_utils.py
from datetime import datetime

def safe_datetime(dt):
    return datetime.fromisoformat(str(dt))
