import os
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.intent_service import parse_intent
from app.services.bill_service import calculate_bill_service
from app.services.billing_service import (
    pay_bill_service,
    get_bill_details_service,
)

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
        if "error" in intent_data:
            return jsonify({"error": "Intent parsing failed", "details": intent_data}), 500
    except Exception as e:
        return jsonify({"error": "Intent parsing failed", "details": str(e)}), 500

    intent = intent_data.get("intent")
    subscriber_no = intent_data.get("subscriber_no")
    month = intent_data.get("month")

    if not intent or not subscriber_no or not month:
        return jsonify({"error": "Missing parsed fields from intent data"}), 400

    if intent == "get_bill":
        # calculate_bill_service 'data' ve 'subscriber_no' bekliyor
        resp, status = calculate_bill_service({"month": month}, subscriber_no)
        return resp, status

    elif intent == "get_bill_details":
        page = 1
        page_size = 10
        resp, status = get_bill_details_service(subscriber_no, month, page, page_size)
        return resp, status

    elif intent == "pay_bill":
        resp, status = pay_bill_service({"subscriber_no": subscriber_no, "month": month})
        return resp, status

    return jsonify({"error": f"Unhandled intent: {intent}"}), 400
