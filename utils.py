import re

def validate_booking_data(data):
    errors = []

    if not data.get("package"):
        errors.append("Package is required")

    if not data.get("travel_date"):
        errors.append("Travel date is required")

    if not data.get("num_travelers"):
        errors.append("Number of travelers is required")

    if not data.get("name"):
        errors.append("Name is required")

    if not data.get("mobile"):
        errors.append("Mobile number is required")

    email = data.get("email")
    if not email:
        errors.append("Email is required")
    else:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Invalid email format")

    return errors
