# handles user registration and login endpoints using JWT authentication
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flasgger import swag_from
from app.services.auth_service import signup_service, login_service

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'description': 'Register a new subscriber',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'subscriber_no': {'type': 'string'},
                    'name': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['subscriber_no', 'name', 'password']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Subscriber created successfully',
            'examples': {
                'application/json': {
                    'message': 'Subscriber created'
                }
            }
        }
    }
})
def signup():
    data = request.get_json()  # get signup form data
    return signup_service(data) # call the signup service with the data

@auth_bp.route("/login", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'description': 'Log in and get JWT token',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'subscriber_no': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['subscriber_no', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'JWT access token',
            'examples': {
                'application/json': {
                    'access_token': 'your.jwt.token'
                }
            }
        },
        401: {
            'description': 'Invalid credentials',
            'examples': {
                'application/json': {
                    'error': 'Invalid credentials'
                }
            }
        }
    }
})
def login():
    data = request.get_json()  # get login form data
    subscriber_no = data.get("subscriber_no")
    password = data.get("password")
    return login_service(subscriber_no, password) # call the login service with the data
