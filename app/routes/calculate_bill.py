# provides an endpoint to calculate a subscriber's bill for a specific month
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.bill_service import calculate_bill_service

bill_bp = Blueprint("bill", __name__)

@bill_bp.route("/calculate-bill", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Billing'],
    'description': 'Calculate monthly bill for the subscriber',
    'security': [{"Bearer": []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'month': {'type': 'string'}
                },
                'required': ['month']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Calculated bill total',
            'examples': {
                'application/json': {
                    'total': 12.5
                }
            }
        }
    }
})
def calculate_bill():
    data = request.get_json()  # get the requested billing month
    subscriber_no = get_jwt_identity() # get user identity from JWT
    return calculate_bill_service(data, subscriber_no) # calculate the bill for the current user
