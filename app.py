from datetime import datetime
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_mail import Mail, Message
from config import Config
from models import db, Booking
from utils import validate_booking_data
import logging

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

CORS(app)
db.init_app(app)
mail = Mail(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables safely
with app.app_context():
    db.create_all()

# ------------------ ROUTES ------------------ #

@app.route('/')
def home():
    return render_template('shaktipeeth-homepage.html')

@app.route('/about')
def about():
    return render_template('about-page.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('shaktipeeth-registration.html')

@app.route('/donation')
def donation():
    return render_template('donation-page.html')

@app.route('/book')
def book_tour_complete():
    return render_template('book-tour.html')

@app.route('/map')
def sacred_map():
    return render_template('sacred-map.html')


# ------------------ API ------------------ #

@app.route('/api/book', methods=['POST'])
def book_tour():
    try:
        data = request.json

        errors = validate_booking_data(data)
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400

        booking = Booking(
            package=data['package'],
            travel_date=datetime.strptime(data['travel_date'], '%Y-%m-%d').date(),
            num_travelers=int(data['num_travelers']),
            accommodation=data['accommodation'],
            special_requirements=data.get('special_requirements', ''),
            contact_person=data['name'],
            mobile=data['mobile'],
            email=data['email']
        )

        db.session.add(booking)
        db.session.commit()

        # Optional email (safe fail)
        try:
            send_confirmation_email(booking)
        except Exception as e:
            logger.warning(f"Email failed: {e}")

        return jsonify({
            'success': True,
            'message': 'Booking successful',
            'booking_id': booking.id
        }), 201

    except Exception as e:
        logger.error(f"Booking error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error'}), 500


def send_confirmation_email(booking):
    if not app.config.get("MAIL_USERNAME"):
        return  # skip if not configured

    msg = Message(
        subject=f"Booking Confirmation - {booking.id}",
        recipients=[booking.email],
        body=f"""
Dear {booking.contact_person},

Your booking is confirmed.

Booking ID: {booking.id}
Package: {booking.package}
Date: {booking.travel_date}

- Shaktipeeth Team
"""
    )
    mail.send(msg)


@app.route('/api/bookings/<int:booking_id>')
def get_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return jsonify(booking.to_dict())


@app.route('/api/bookings')
def get_bookings():
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return jsonify([b.to_dict() for b in bookings])


# ------------------ RUN ------------------ #

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
