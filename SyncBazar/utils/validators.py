"""
Input validation utilities
"""

def validate_email(email):
    """Validate email format"""
    if not email or '@' not in email:
        return False
    return True


def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, ""


def validate_numeric(value, field_name):
    """Validate numeric input"""
    try:
        num = float(value)
        if num < 0:
            return False, f"{field_name} cannot be negative"
        return True, num
    except ValueError:
        return False, f"{field_name} must be a number"


def validate_item_data(item_data):
    """Validate item data"""
    errors = []
    
    if not item_data.get('name', '').strip():
        errors.append("Item name is required")
    
    quantity_valid, quantity_msg = validate_numeric(item_data.get('quantity', 0), "Quantity")
    if not quantity_valid:
        errors.append(quantity_msg)
    
    price_valid, price_msg = validate_numeric(item_data.get('price', 0), "Price")
    if not price_valid:
        errors.append(price_msg)
    
    return errors
