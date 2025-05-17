# handles billing operations including payment, history and detailed usage breakdown
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.billing_service import (
    pay_bill_service,
    get_paid_bills_service,
    get_bill_details_service
)

billing_bp = Blueprint("billing", __name__)

@billing_bp.route("", methods=["POST"])
@swag_from({
    'tags': ['Billing'],
    'description': 'Pay a bill for a given month (No authentication required)',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'subscriber_no': {'type': 'string'},
                    'month': {'type': 'string'}
                },
                'required': ['subscriber_no', 'month']
            }
        }
    ],
    'responses': {
        200: {'description': 'Bill paid successfully or topped up'},
        400: {'description': 'No usage to pay for'}
    }
})
def pay_bill():
    data = request.get_json()
    return pay_bill_service(data)

@billing_bp.route("/bill", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Billing'],
    'description': 'List all paid bills for the logged-in subscriber',
    'security': [{"Bearer": []}],
    'responses': {
        200: {
            'description': 'List of paid bills',
            'examples': {
                'application/json': [
                    {
                        "month": "2025-04",
                        "total": 3.0,
                        "paid_at": "2025-04-20T14:33:00"
                    }
                ]
            }
        }
    }
})
def get_paid_bills():
    subscriber_no = get_jwt_identity() # get user identity from JWT
    return get_paid_bills_service(subscriber_no) # get all paid bills for the current user

@billing_bp.route("/bill/details", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Billing'],
    'description': 'Get detailed breakdown of usage and bill for a specific month',
    'security': [{"Bearer": []}],
    'parameters': [
        {
            'name': 'month',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Month in YYYY-MM format (e.g. 2025-04)'
        },
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Pagination page number (default: 1)'
        },
        {
            'name': 'page_size',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Number of usage items per page (default: 10)'
        }
    ],
    'responses': {
        200: {
            'description': 'Detailed bill info with usage breakdown and remaining amount if applicable',
            'examples': {
                'application/json': {
                    "month": "2025-04",
                    "paid": True,
                    "total": 30,
                    "paid_total": 20,
                    "remaining_due": 10,
                    "details": {
                        "items": [
                            {"type": "phone", "amount": 2},
                            {"type": "internet", "amount": 1}
                        ],
                        "current_page": 1,
                        "page_size": 2,
                        "total_items": 3,
                        "total_pages": 2
                    }
                }
            }
        }
    }
})
def get_bill_details():
    subscriber_no = get_jwt_identity()
    month = request.args.get("month")  # target billing month
    page = int(request.args.get("page", 1)) # pagination page number
    page_size = int(request.args.get("page_size", 10)) # items per page	
    return get_bill_details_service(subscriber_no, month, page, page_size) # get detailed bill info for the current user
