# handles the business logic for signup and login using jwt authentication
from app.extensions import db
from app.models.subscriber import Subscriber
from flask import jsonify
from flask_jwt_extended import create_access_token

def signup_service(data):
    subscriber_no = data.get("subscriber_no")
    name = data.get("name")
    password = data.get("password")

    # check if subscriber already exists
    if Subscriber.query.get(subscriber_no):
        return jsonify({"error": "Subscriber already exists"}), 400

    # create new subscriber and hash password
    subscriber = Subscriber(subscriber_no=subscriber_no, name=name)
    subscriber.set_password(password)
    db.session.add(subscriber)
    db.session.commit()

    return jsonify({"message": "Subscriber created"}), 201

def login_service(subscriber_no, password):
    # check if subscriber exists and password is correct
    subscriber = Subscriber.query.get(subscriber_no)
    if not subscriber or not subscriber.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # generate jwt token
    access_token = create_access_token(identity=subscriber_no)
    return jsonify(access_token=access_token), 200
