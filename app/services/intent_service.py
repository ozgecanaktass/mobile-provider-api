# app/services/intent_service.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_intent(message):
    """
    Given a user message, returns a dict with intent and parameters
    Example output:
    {
        "intent": "get_bill",
        "subscriber_no": "12345",
        "month": "2025-03"
    }
    """
    system_prompt = """
    You are an assistant for a mobile billing system. 
    Extract the user's intent and any required parameters from their message.
    Respond in this format:
    intent=<intent_name>; subscriber_no=<subscriber_no>; month=<YYYY-MM>
    Example: intent=get_bill; subscriber_no=12345; month=2025-03
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    )

    content = response["choices"][0]["message"]["content"]
    parsed = {}
    for part in content.split(";"):
        if "=" in part:
            key, value = part.strip().split("=")
            parsed[key.strip()] = value.strip()

    return parsed
