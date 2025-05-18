import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_intent(user_message):
    """
    Calls OpenAI's Chat API to determine intent and extract parameters
    """
    response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": (
                "You are an AI that extracts structured intent and billing data from user messages. "
                "You MUST respond ONLY with a JSON object containing: "
                "{intent: string, subscriber_no: string, month: YYYY-MM}. "
                "Do NOT include any explanation or extra text. Respond with pure JSON only."
            )
        },
        {
            "role": "user",
            "content": f"{user_message}"
        }
    ]
)


    content = response.choices[0].message.content

    # Expected format in the response: JSON string
    # Example: {"intent": "get_bill", "subscriber_no": "12345", "month": "2025-03"}
    try:
        import json
        parsed = json.loads(content)
        return parsed
    except Exception as e:
        return {"error": "Failed to parse intent JSON", "raw_response": content, "exception": str(e)}
