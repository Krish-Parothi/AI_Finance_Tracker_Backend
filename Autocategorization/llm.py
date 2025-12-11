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
