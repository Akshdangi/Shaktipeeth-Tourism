from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text, nullable=False)
    idtype = db.Column(db.String(50), nullable=False)
    idnumber = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'fullname': self.fullname,
            'age': self.age,
            'address': self.address,
            'idtype': self.idtype,
            'idnumber': self.idnumber,
            'mobile': self.mobile,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package = db.Column(db.String(50), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    num_travelers = db.Column(db.Integer, nullable=False)
    accommodation = db.Column(db.String(20), nullable=False)
    special_requirements = db.Column(db.Text)
    contact_person = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

    def to_dict(self):
        return {
            'id': self.id,
            'package': self.package,
            'travel_date': self.travel_date.strftime('%Y-%m-%d'),
            'num_travelers': self.num_travelers,
            'accommodation': self.accommodation,
            'special_requirements': self.special_requirements,
            'contact_person': self.contact_person,
            'mobile': self.mobile,
            'email': self.email,
            'booking_date': self.booking_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status
        }

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    assistant_reply = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_message': self.user_message,
            'assistant_reply': self.assistant_reply,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }