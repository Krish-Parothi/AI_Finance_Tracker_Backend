from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import json, os
from dotenv import load_dotenv
load_dotenv()

SYSTEM_PROMPT = '''
You are an expense extraction assistant. From the input paragraph, extract **all expenses** and return **only a valid JSON array**. No extra text.  

Each expense object must have the following keys:
- "amount": number only, extracted from text
- "category": one of ["Food", "Travel", "Groceries", "Shopping", "Entertainment", "Bills", "Medical", "Education", "Other"]
- "merchant": string if mentioned, otherwise null
- "description": short description of the expense
- "date": date in "YYYY-MM-DD" format if mentioned, otherwise "today"

Rules:
1. Extract multiple expenses from a single sentence if present.
2. Do not include duplicates.
3. Ignore any unrelated numbers.
4. Return JSON strictly, no extra commentary or text.

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
        res = self.model.invoke(msg).content.strip()
        try: return json.loads(res)
        except:
            try: return json.loads(res[res.index("["): res.rindex("]")+1])
            except: return []
