# service functions for creating and listing usage data
from flask import jsonify
from app.models.usage_model import Usage
from app.extensions import db

# Add 10 minutes of phone
# Add 1 MB of Internet 

def add_usage_service(data, subscriber_no):
    """adds a new usage entry for the current user"""
    month = data.get("month")
    usage_type = data.get("type")
    amount = data.get("amount", 1)  # default amount = 1

    if usage_type not in ["phone", "internet"]:
        return jsonify({"error": "Invalid usage type"}), 400

    # create new usage entry with specified or default amount
    usage = Usage(
        subscriber_no=subscriber_no,
        month=month,
        type=usage_type,
        amount=amount
    )
    db.session.add(usage)
    db.session.commit()
    return jsonify({"message": "Usage added"}), 200

def list_usage_service(subscriber_no):
    """returns all usage records for the current user"""
    usages = Usage.query.filter_by(subscriber_no=subscriber_no).all()

    result = [{
        "subscriber_no": u.subscriber_no,
        "month": u.month,
        "type": u.type,
        "amount": u.amount
    } for u in usages]

    return jsonify(result), 200
