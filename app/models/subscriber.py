# defines the subscriber model and password handling functions
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Subscriber(db.Model):
    __tablename__ = "subscriber"

    subscriber_no = db.Column(db.String(20), primary_key=True)  # unique id for each subscriber
    name = db.Column(db.String(100), nullable=False)  # subscriber's name
    password_hash = db.Column(db.String(256), nullable=False)  # encrypted password

    def set_password(self, password):
        # hashes the given plain-text password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # checks if entered password matches the stored hash
        return check_password_hash(self.password_hash, password)
