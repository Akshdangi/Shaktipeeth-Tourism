import sys
import os

# 🔥 FORCE Python to detect project root (FIXES ml import issue)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from datetime import datetime
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from flask_mail import Mail, Message
from config import Config
from models import db, Booking, User, ChatMessage
from utils import validate_booking_data, validate_registration_data
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

CORS(app, supports_credentials=True)
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

@app.route('/logout')
def logout_page():
    return render_template('logout.html')

@app.route('/register')
def register():
    return render_template('shaktipeeth-registration.html')

@app.route('/donation')
def donation():
    return render_template('donation-page.html')

@app.route('/book')
def book_tour_complete():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('book-tour-complete.html')

@app.route('/map')
def sacred_map():
    return render_template('sacred-map.html')


# ------------------ ML API ------------------ #

# ------------------ CHATBOT API (OLLAMA) ------------------ #

@app.route('/api/chat', methods=['POST'])
def chat():
    import urllib.request
    import json
    
    try:
        data = request.json or {}
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"success": False, "error": "Message is required"}), 400

        # Query local Ollama running shaktigpt
        payload = {
            "model": "shaktigpt",
            "messages": [
                {"role": "user", "content": user_message}
            ],
            "stream": False
        }
        
        # Use configured Ollama / LLM API URL (can be set via OLLAMA_API_URL env var)
        ollama_url = app.config.get('OLLAMA_API_URL', 'http://35.192.53.123:11434/api/chat')
        req = urllib.request.Request(
            ollama_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            assistant_message = res_data.get("message", {}).get("content", "")
            return jsonify({
                "success": True,
                "reply": assistant_message
            })
            
    except Exception as e:
        logger.error(f"Ollama chat error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Could not connect to Ollama. Make sure Ollama is running and 'shaktigpt' model is created."
        }), 500


@app.route('/api/save-chat', methods=['POST'])
def save_chat():
    try:
        if 'user_id' not in session:
            return jsonify({"success": False, "error": "Please login to save chat"}), 401
        
        data = request.json or {}
        user_message = data.get("user_message", "")
        assistant_reply = data.get("assistant_reply", "")
        
        if not user_message or not assistant_reply:
            return jsonify({"success": False, "error": "Both messages are required"}), 400
        
        chat_message = ChatMessage(
            user_id=session['user_id'],
            user_message=user_message,
            assistant_reply=assistant_reply
        )
        
        db.session.add(chat_message)
        db.session.commit()
        
        return jsonify({"success": True, "message": "Chat saved successfully"}), 201
        
    except Exception as e:
        logger.error(f"Save chat error: {str(e)}")
        return jsonify({"success": False, "error": "Failed to save chat"}), 500


@app.route('/api/chat-history', methods=['GET'])
def get_chat_history():
    try:
        if 'user_id' not in session:
            return jsonify({"success": False, "error": "Please login to view chat history"}), 401
        
        messages = ChatMessage.query.filter_by(user_id=session['user_id']).order_by(ChatMessage.created_at.desc()).limit(50).all()
        
        return jsonify({
            "success": True,
            "history": [msg.to_dict() for msg in reversed(messages)]
        }), 200
        
    except Exception as e:
        logger.error(f"Get chat history error: {str(e)}")
        return jsonify({"success": False, "error": "Failed to retrieve chat history"}), 500


# ------------------ AUTH API ------------------ #

@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.json or {}
        errors = validate_registration_data(data)
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400

        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email'].lower()).first()
        if existing_user:
            return jsonify({'success': False, 'errors': ['Email is already registered']}), 400

        # Hash password and create user
        password_hash = generate_password_hash(data['password'])
        new_user = User(
            fullname=data['fullname'],
            age=int(data['age']),
            address=data['address'],
            idtype=data['idtype'],
            idnumber=data['idnumber'],
            mobile=data['mobile'],
            email=data['email'].lower(),
            password_hash=password_hash
        )

        db.session.add(new_user)
        db.session.commit()

        try:
            send_registration_email(new_user)
        except Exception as e:
            logger.warning(f"Registration email failed: {e}")

        return jsonify({
            'success': True,
            'message': 'Registration successful!'
        }), 201

    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500


@app.route('/api/login', methods=['POST'])
def login_user():
    try:
        data = request.json or {}
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and Password are required'}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

        # Store user details in session
        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_name'] = user.fullname

        return jsonify({
            'success': True,
            'message': 'Login successful!',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500


@app.route('/api/logout', methods=['POST', 'GET'])
def logout_user():
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('user_name', None)
    return jsonify({
        'success': True,
        'message': 'Logged out successfully!'
    }), 200


@app.route('/api/user-status')
def user_status():
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user': {
                'id': session['user_id'],
                'email': session['user_email'],
                'name': session['user_name']
            }
        }), 200
    return jsonify({
        'logged_in': False
    }), 200


# ------------------ BOOKING API ------------------ #

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
        logger.warning("MAIL_USERNAME not set. Booking confirmation email skipped.")
        return

    admin_email = app.config.get("MAIL_USERNAME")
    recipients = [booking.email]
    
    # Send a copy to the admin if it's different from the booking email
    if admin_email and admin_email.lower() not in [r.lower() for r in recipients]:
        recipients.append(admin_email)

    msg = Message(
        subject=f"Booking Confirmation - Tour Booking ID #{booking.id}",
        sender=admin_email,
        recipients=recipients,
        body=f"""Dear {booking.contact_person},

Jai Mata Di! 🙏

Your booking with Shaktipeeth Tourism has been successfully confirmed. We are excited to assist you on your spiritual journey!

Here are the booking details:
- Booking ID: #{booking.id}
- Package Name: {booking.package}
- Travel Date: {booking.travel_date.strftime('%Y-%m-%d') if booking.travel_date else 'N/A'}
- Number of Travelers: {booking.num_travelers}
- Accommodation: {booking.accommodation}
- Special Requirements: {booking.special_requirements or 'None'}

Contact Details:
- Mobile: {booking.mobile}
- Email: {booking.email}

If you have any questions or need to make changes to your booking, please contact us at {admin_email}.

Wishing you a divine and blessed pilgrimage!

Warm regards,
Shaktipeeth Tourism Team"""
    )
    mail.send(msg)


def send_registration_email(user):
    if not app.config.get("MAIL_USERNAME"):
        logger.warning("MAIL_USERNAME not set. Registration confirmation email skipped.")
        return

    msg = Message(
        subject="Welcome to Shaktipeeth Tourism - Registration Confirmation",
        sender=app.config.get("MAIL_USERNAME"),
        recipients=[user.email],
        body=f"""Dear {user.fullname},

Jai Mata Di! 🙏

Welcome to Shaktipeeth Tourism! Your registration has been successfully processed.

Here are your account details:
- Email: {user.email}
- Mobile: {user.mobile}
- Government ID Type: {user.idtype}
- Registered On: {user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else 'N/A'}

You can now log in to plan your sacred journeys, explore packages, and book tours.

Warm regards,
Shaktipeeth Tourism Team"""
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
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8001)), debug=True)
