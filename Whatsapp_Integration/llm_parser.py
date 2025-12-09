from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_template(
"""
Convert the raw expense message into a JSON array of expense objects.

Rules:
- Each expense (food, travel, hotel, shopping, etc.) must be a separate object.
- amount: number
- category: inferred from text
- description: short summary of that expense
- timestamp: current UTC if not given
- source = "whatsapp"
- metadata = {{}}

Output JSON array only. Each entry must be a separate object.
Do not combine multiple expenses into one.

Message: {message}
"""
)


def parse_text(message: str):
    chain = prompt | model
    raw = chain.invoke({"message": message}).content.strip()

    try:
        data_list = json.loads(raw)
        if not isinstance(data_list, list):
            data_list = [data_list]
    except:
        data_list = [{
            "amount": None,
            "category": "unknown",
            "description": message,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "whatsapp",
            "metadata": {}
        }]

    for entry in data_list:
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.utcnow().isoformat()
        entry["source"] = "whatsapp"

    return data_list
#llm_parser.py