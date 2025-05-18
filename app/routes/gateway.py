import os
import openai
from dotenv import load_dotenv
import json

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_intent(user_message):
    """
    Calls OpenAI's Chat API to determine intent and extract parameters.
    Only returns one of the following intents:
    - get_bill
    - get_bill_details
    - pay_bill
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that extracts billing-related intent from user queries.\n"
                    "You must respond ONLY with a JSON object in the following exact format:\n"
                    "{\"intent\": one of [\"get_bill\", \"get_bill_details\", \"pay_bill\"], \"subscriber_no\": string, \"month\": YYYY-MM}.\n"
                    "If the message is ambiguous or irrelevant, choose \"intent\": \"get_bill\" by default.\n"
                    "Respond with JSON only. Do not include any explanation, notes, or text."
                )
            },
            {
                "role": "user",
                "content": f"{user_message}"
            }
        ]
    )

    content = response.choices[0].message.content

    try:
        parsed = json.loads(content)
        return parsed
    except Exception as e:
        return {
            "error": "Failed to parse intent JSON",
            "raw_response": content,
            "exception": str(e)
        }
