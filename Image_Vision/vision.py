import base64
import json
import os
from groq import Groq

# Initialize Groq client using environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def parse_bill(image_bytes: bytes):
    """
    Parse an uploaded bill image and return structured expenses.
    Returns a list of dicts: description, amount, category, timestamp, metadata.
    """
    b64_image = base64.b64encode(image_bytes).decode()

    prompt = """
    Extract all expenses from this bill image.
    Output strictly as a JSON array.
    Each object must contain: description, amount, category, timestamp, metadata.
    Allowed categories: Food, Travel, Groceries, Shopping, Entertainment, Bills, Medical, Education, Other.
    """

    response = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{b64_image}"
                    }
                }
            ]
        }],
        temperature=0
    )

    try:
        content = response.choices[0].message.content
        # Remove potential markdown code blocks
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        return json.loads(content)
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(f"Response content: {response.choices[0].message.content}")
        return []