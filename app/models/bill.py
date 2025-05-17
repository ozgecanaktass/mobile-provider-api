# defines the database model for billing records

from app.extensions import db

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique bill id
    subscriber_no = db.Column(db.String(20), nullable=False) 
    month = db.Column(db.String(7), nullable=False)  # billing period 
    total = db.Column(db.Float, nullable=False)  # total amount to be paid
    paid_at = db.Column(db.DateTime, nullable=False)  # date and time of payment
