from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_mail import Mail, Message
from config import Config
from models import db, Booking
from utils import validate_booking_data
import logging

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
app.config['TEMPLATES_AUTO_RELOAD'] = True  # auto reload templates

CORS(app)
db.init_app(app)
mail = Mail(app)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create DB tables
with app.app_context():
    db.create_all()

# ------------------ FRONTEND ROUTES ------------------ #

@app.route('/')
def home():
    return render_template('shaktipeeth-homepage.html')


@app.route('/about')
def about():   # matches url_for('about')
    return render_template('about-page.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():   # matches url_for('register')
    return render_template('shaktipeeth-registration.html')


@app.route('/donation')
def donation():   # matches url_for('donation')
    return render_template('donation-page.html')


# ✅ ADD THESE (your HTML was calling them)
@app.route('/map')
def sacred_map():
    return render_template('sacred-map.html')

@app.route('/book')
def book_tour_complete():
    return render_template('book-tour-complete.html') # create this file


# ------------------ API ROUTES ------------------ #

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

        try:
            send_confirmation_email(booking)
        except Exception as e:
            logger.error(f"Email failed: {str(e)}")

        return jsonify({
            'success': True,
            'message': 'Booking successful',
            'booking_id': booking.id
        }), 201

    except Exception as e:
        logger.error(f"Booking error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Server error'
        }), 500


def send_confirmation_email(booking):
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


@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return jsonify(booking.to_dict())


@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return jsonify([b.to_dict() for b in bookings])


# ------------------ RUN ------------------ #

if __name__ == '__main__':
    app.run(debug=True, port=8000)