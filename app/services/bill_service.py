# calculates the total bill amount based on phone and internet usage
from flask import jsonify
from app.models.usage_model import Usage

def calculate_bill_service(data, subscriber_no):
    """calculates monthly bill for the subscriber"""
    month = data.get("month")

    usages = Usage.query.filter_by(subscriber_no=subscriber_no, month=month).all()

    phone_minutes = 0
    internet_mb = 0

    # calculate total usage
    for usage in usages:
        if usage.type == "phone":
            phone_minutes += usage.amount * 10  # 1 usage = 10 minutes
        elif usage.type == "internet":
            internet_mb += usage.amount         # 1 usage = 1 MB

    total = 0

    # phone: first 1000 minutes free, then every 1000 min = $10
    if phone_minutes > 1000:
        extra_minutes = phone_minutes - 1000
        total += (extra_minutes // 1000) * 10

    # internet: first 20GB = $50, extra every 10GB = $10
    if internet_mb > 0:
        total += 50
        if internet_mb > 20000:
            extra_mb = internet_mb - 20000
            total += (extra_mb // 10000) * 10

    return jsonify({
        "total": total,
        "phone_minutes": phone_minutes,
        "internet_mb": internet_mb
    }), 200
