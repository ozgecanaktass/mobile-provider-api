# handles all billing logic including payment, listing and detailed bill breakdown
from flask import jsonify
from datetime import datetime
from app.extensions import db
from app.models.bill import Bill
from app.models.usage_model import Usage

def pay_bill_service(data):
    subscriber_no = data.get("subscriber_no")
    month = data.get("month")

    # fetch usage records for the given subscriber and month
    usages = Usage.query.filter_by(subscriber_no=subscriber_no, month=month).all()
    if not usages:
        return jsonify({"error": "No usage found for this month"}), 400

    # sum total phone and internet usage
    phone_minutes = sum(u.amount for u in usages if u.type == "phone") * 10
    internet_mb = sum(u.amount for u in usages if u.type == "internet")

    # calculate total bill based on pricing rules
    total = 0
    if phone_minutes > 1000:
        total += ((phone_minutes - 1000) // 1000) * 10
    if internet_mb > 0:
        total += 50  # flat rate for first 20GB
        if internet_mb > 20000:
            total += ((internet_mb - 20000) // 10000) * 10

    # check if bill already exists for this month
    bill = Bill.query.filter_by(subscriber_no=subscriber_no, month=month).first()

    if bill:
        # user already paid something — check if there's any remaining due -> top-up logic
        remaining = total - bill.total
        if remaining > 0:
            bill.total += remaining
            bill.paid_at = datetime.utcnow()
            db.session.commit()
            return jsonify({"message": "Remaining bill amount paid", "new_total": bill.total}), 200
        return jsonify({"message": "Already fully paid", "total": bill.total}), 200

    # create new bill entry
    new_bill = Bill(
        subscriber_no=subscriber_no,
        month=month,
        total=total,
        paid_at=datetime.utcnow()
    )
    db.session.add(new_bill)
    db.session.commit()
    return jsonify({"message": "Bill paid successfully", "total": total}), 200

def get_paid_bills_service(subscriber_no):
    # fetch all paid bills for this subscriber
    bills = Bill.query.filter_by(subscriber_no=subscriber_no).all()
    result = [{
        "month": b.month,
        "total": b.total,
        "paid_at": b.paid_at.isoformat()
    } for b in bills]
    return jsonify(result), 200

def get_bill_details_service(subscriber_no, month, page, page_size):
    # get all usage records for this month
    offset = (page - 1) * page_size
    all_usages = Usage.query.filter_by(subscriber_no=subscriber_no, month=month).all()

    # pagination values
    total_items = len(all_usages)
    total_pages = (total_items + page_size - 1) // page_size
    paginated_usages = all_usages[offset:offset + page_size]

    # calculate total usage
    phone_amt = sum(u.amount for u in all_usages if u.type == "phone")
    internet_amt = sum(u.amount for u in all_usages if u.type == "internet")
    phone_minutes = phone_amt * 10
    internet_mb = internet_amt

    # Calculates bill for given month for
    # given subscriber
    # Minutes of Phone Calls – 1000
    # minutes free. Each 1000 minutes is
    # 10$ after
    # Internet Usage – 50$ up to 20GB,
    # 10$ for each 10GB after
    total = 0
    if phone_minutes > 1000:
        total += ((phone_minutes - 1000) // 1000) * 10
    if internet_mb > 0:
        total += 50
        if internet_mb > 20000:
            total += ((internet_mb - 20000) // 10000) * 10

    # get bill info -> if previously paid
    bill = Bill.query.filter_by(subscriber_no=subscriber_no, month=month).first()
    paid = bool(bill)
    paid_total = bill.total if bill else 0
    remaining_due = max(0, total - paid_total)

    # convert MB to GB for display
    def format_data(mb):
        return f"{round(mb / 1000, 2)} GB" if mb >= 1000 else f"{mb} MB"

    return jsonify({
        "month": month,
        "paid": paid,
        "total": total,
        "paid_total": paid_total,
        "remaining_due": remaining_due,
        "details": {
            "items": [{"type": u.type, "amount": u.amount} for u in paginated_usages],
            "current_page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    }), 200
