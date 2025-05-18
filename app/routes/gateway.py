import os
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.intent_service import parse_intent
import requests

GATEWAY_API_BASE = os.getenv("API_BASE_URL", "http://localhost:5000/api/v1")

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
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Missing 'message' in request"}), 400

    try:
        intent_data = parse_intent(user_message)
    except Exception as e:
        return jsonify({"error": "Intent parsing failed", "details": str(e)}), 500

    intent = intent_data.get("intent")
    subscriber_no = intent_data.get("subscriber_no")
    month = intent_data.get("month")

    if not intent or not subscriber_no or not month:
        return jsonify({"error": "Missing parsed fields from intent data"}), 400

    if intent == "get_bill":
        resp = requests.get(f"{GATEWAY_API_BASE}/pay-bill/bill", params={
            "subscriber_no": subscriber_no,
            "month": month
        })
        return jsonify(resp.json()), resp.status_code

    elif intent == "get_bill_details":
        resp = requests.get(f"{GATEWAY_API_BASE}/pay-bill/bill/details", params={
            "subscriber_no": subscriber_no,
            "month": month,
            "page": 1,
            "page_size": 10
        })
        return jsonify(resp.json()), resp.status_code

    elif intent == "pay_bill":
        resp = requests.post(f"{GATEWAY_API_BASE}/pay-bill", json={
            "subscriber_no": subscriber_no,
            "month": month
        })
        return jsonify(resp.json()), resp.status_code

    return jsonify({"error": f"Unhandled intent: {intent}"}), 400
