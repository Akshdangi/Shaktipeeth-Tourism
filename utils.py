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


def validate_registration_data(data):
    errors = []

    if not data.get("fullname"):
        errors.append("Full name is required")

    try:
        age = int(data.get("age", 0))
        if age < 18 or age > 120:
            errors.append("Age must be between 18 and 120")
    except (ValueError, TypeError):
        errors.append("Valid age is required")

    if not data.get("address"):
        errors.append("Address is required")

    if not data.get("idtype"):
        errors.append("Government ID type is required")

    if not data.get("idnumber"):
        errors.append("Government ID number is required")

    if not data.get("mobile"):
        errors.append("Mobile number is required")
    elif not re.match(r"^\d{10}$", str(data.get("mobile"))):
        errors.append("Mobile number must be exactly 10 digits")

    email = data.get("email")
    if not email:
        errors.append("Email is required")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append("Invalid email format")

    password = data.get("password")
    if not password:
        errors.append("Password is required")
    elif len(password) < 6:
        errors.append("Password must be at least 6 characters long")

    return errors