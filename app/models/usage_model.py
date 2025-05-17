# defines the usage model storing phone or internet usage records
from app.extensions import db

class Usage(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique usage id
    subscriber_no = db.Column(db.String(20), nullable=False) 
    month = db.Column(db.String(7), nullable=False)  
    type = db.Column(db.String(20), nullable=False)  # phone or internet
    amount = db.Column(db.Integer, default=1)  # usage amount ( 1 = 10 min for phone usage or 1 MB for internet usage)
