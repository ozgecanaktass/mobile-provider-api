import os
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.intent_service import parse_intent
import requests
import traceback

GATEWAY_API_BASE = os.getenv("API_BASE_URL", "https://mobile-provider-api-vfpp.onrender.com/api/v1")
TEST_JWT = os.getenv("TEST_JWT") 

gateway_bp = Blueprint("gateway", __name__)

@gateway_bp.route("/chat", methods=["POST"])
@swag_from({
    "tags": ["Gateway"],
    "description": "Chat endpoint that receives a natural language message and routes it to the correct billing API based on detected intent.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "What is the bill for subscriber 12345 for March 2025?"
                    }
                },
                "required": ["message"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "Intent matched and API responded successfully"
        },
        400: {
            "description": "Bad request or missing intent parameters"
        },
        500: {
            "description": "Internal server error (e.g. intent parsing failed)"
        }
    }
})
def chat():
    print("GATEWAY: Yeni istek geldi!")
    data = request.get_json()
    print("GATEWAY: Gelen veri:", data)

    user_message = data.get("message")

    if not user_message:
        print("GATEWAY ERROR: message parametresi eksik.")
        return jsonify({"error": "Missing 'message' in request"}), 400

    try:
        intent_data = parse_intent(user_message)
        print("GATEWAY: Intent parse sonucu:", intent_data)
        if "error" in intent_data:
            print("GATEWAY ERROR: Intent parse hatası:", intent_data)
            return jsonify({"error": "Intent parsing failed", "details": intent_data}), 500
    except Exception as e:
        print("GATEWAY EXCEPTION (parse_intent):")
        print(traceback.format_exc())
        return jsonify({"error": "Intent parsing failed", "details": str(e)}), 500

    intent = intent_data.get("intent")
    subscriber_no = intent_data.get("subscriber_no")
    month = intent_data.get("month")

    if not intent or not subscriber_no or not month:
        print("GATEWAY ERROR: Parsed fields eksik.", intent, subscriber_no, month)
        return jsonify({"error": "Missing parsed fields from intent data"}), 400

    # JWT token header
    headers = {
        "Authorization": f"Bearer {TEST_JWT}"
    }
    print(f"GATEWAY: Yönlendirilecek intent: {intent}")

    try:
        if intent == "get_bill":
            print("GATEWAY: get_bill çağrılıyor.")
            resp = requests.get(
                f"{GATEWAY_API_BASE}/pay-bill/bill",
                params={
                    "subscriber_no": subscriber_no,
                    "month": month
                },
                headers=headers
            )
            print("GATEWAY: get_bill API cevabı:", resp.status_code, resp.text)
            return jsonify(resp.json()), resp.status_code

        elif intent == "get_bill_details":
            print("GATEWAY: get_bill_details çağrılıyor.")
            resp = requests.get(
                f"{GATEWAY_API_BASE}/pay-bill/bill/details",
                params={
                    "subscriber_no": subscriber_no,
                    "month": month,
                    "page": 1,
                    "page_size": 10
                },
                headers=headers
            )
            print("GATEWAY: get_bill_details API cevabı:", resp.status_code, resp.text)
            return jsonify(resp.json()), resp.status_code

        elif intent == "pay_bill":
            print("GATEWAY: pay_bill çağrılıyor.")
            resp = requests.post(
                f"{GATEWAY_API_BASE}/pay-bill",
                json={
                    "subscriber_no": subscriber_no,
                    "month": month
                },
                headers=headers
            )
            print("GATEWAY: pay_bill API cevabı:", resp.status_code, resp.text)
            return jsonify(resp.json()), resp.status_code

        else:
            print(f"GATEWAY ERROR: Bilinmeyen intent: {intent}")
            return jsonify({"error": f"Unhandled intent: {intent}"}), 400

    except Exception as e:
        print("GATEWAY EXCEPTION (API çağrısı):")
        print(traceback.format_exc())
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
