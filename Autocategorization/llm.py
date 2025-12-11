# Autocategorization/llm.py
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import json, os
from dotenv import load_dotenv
load_dotenv()

SYSTEM_PROMPT = '''
You are an expense extraction assistant. From the input paragraph, extract all expenses 
and return ONLY a valid JSON array.

Each expense object must contain:
- "amount": number
- "category": one of ["Food","Travel","Groceries","Shopping","Entertainment","Bills","Medical","Education","Other"]
- "description": short text about the expense
- "timestamp": "YYYY-MM-DD" format
- "source": always "auto"

Rules:
1. Extract multiple expenses.
2. No duplicates.
3. Ignore irrelevant numbers.
4. Return strictly JSON array, nothing else.
5. If no expenses found, return exactly [] and never create empty objects.
'''

USER_PROMPT = "{paragraph}"


class LLMExtractor:
    def __init__(self):
        self.model = ChatGroq(
            groq_api_key=os.getenv("VA_GROQ_API_KEY"),
            model="openai/gpt-oss-120b",
            temperature=0
        )
        self.prompt = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("user", USER_PROMPT)])

    def extract(self, paragraph: str):
        msg = self.prompt.format_messages(paragraph=paragraph)
        raw = self.model.invoke(msg).content.strip()

        # ---------------------------
        # structural validation
        # ---------------------------
        def safe_load(text):
            try:
                data = json.loads(text)
                if isinstance(data, list):
                    return data
            except:
                return None
            return None

        data = safe_load(raw)
        if data is None and "[" in raw and "]" in raw:
            segment = raw[raw.index("["): raw.rindex("]")+1]
            data = safe_load(segment)
        if data is None:
            return []

        # ---------------------------
        # semantic cleaning
        # ---------------------------
        cleaned = []
        for d in data:
            if not isinstance(d, dict):
                continue
            amt = d.get("amount")
            desc = d.get("description")
            cat = d.get("category")
            if (
                isinstance(amt, (int, float)) and amt > 0 and
                isinstance(desc, str) and desc.strip() != "" and
                isinstance(cat, str) and cat.strip() != ""
            ):
                cleaned.append(d)

        return cleaned
