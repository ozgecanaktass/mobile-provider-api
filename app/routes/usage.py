# handles usage creation and retrieval for the logged-in subscriber
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.usage_service import add_usage_service, list_usage_service

usage_bp = Blueprint("usage", __name__)

@usage_bp.route("", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Usage'],
    'description': 'Add a new usage record (call or internet)',
    'security': [{"Bearer": []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'month': {'type': 'string'},
                    'type': {'type': 'string', 'enum': ['phone', 'internet']}
                },
                'required': ['month', 'type']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Usage successfully added',
            'examples': {
                'application/json': {
                    'message': 'Usage added'
                }
            }
        },
        401: {
            'description': 'Unauthorized – Token missing or invalid',
            'examples': {
                'application/json': {
                    'msg': 'Missing Authorization Header'
                }
            }
        }
    }
})
def add_usage():
    data = request.get_json()  # get usage data from request body	
    subscriber_no = get_jwt_identity()  # get user identity from JWT
    return add_usage_service(data, subscriber_no)  # add usage record for the current user

@usage_bp.route("", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Usage'],
    'description': 'List usage records for the current subscriber',
    'security': [{"Bearer": []}],
    'responses': {
        200: {
            'description': 'List of usage records',
            'examples': {
                'application/json': [
                    {
                        "subscriber_no": "12345",
                        "month": "2025-04",
                        "type": "phone",
                        "amount": 3
                    }
                ]
            }
        }
    }
})
def list_usage():
    subscriber_no = get_jwt_identity()  # get user identity from JWT	
    return list_usage_service(subscriber_no)  # list all usage records for the current user