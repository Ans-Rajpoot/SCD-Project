"""
Helper functions for SyncBazar
"""
import datetime
from config import APP_SETTINGS


def format_currency(amount):
    """Format amount as currency"""
    try:
        return f"Rs. {float(amount):,.2f}"
    except:
        return "Rs. 0.00"


def format_date(date_obj):
    """Format date object"""
    if isinstance(date_obj, datetime.datetime):
        return date_obj.strftime("%Y-%m-%d %H:%M")
    elif isinstance(date_obj, str):
        return date_obj
    return ""


def get_theme_color(color_name):
    """Get theme color"""
    return APP_SETTINGS['theme'].get(color_name, '#000000')


def calculate_total_value(quantity, price):
    """Calculate total value"""
    try:
        return float(quantity) * float(price)
    except:
        return 0.0


def truncate_text(text, max_length=50):
    """Truncate text with ellipsis"""
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    return text
