"""
Configuration file for SyncBazar Inventory System
"""

# Database Configuration

# File: config.py
DB_CONFIG = {
    'server': 'localhost\\SQLEXPRESS',
    'database': 'Bazar_db',
    'username': '',    # Windows Authentication
    'password': '',
    'trusted_connection': 'yes',
    'driver': 'ODBC Driver 17 for SQL Server'
}

# Application Settings
APP_SETTINGS = {
    'title': 'SyncBazar - Inventory Management System',
    'geometry': '1200x700',
    'theme': {
        'bg': '#f0f0f0',
        'fg': '#333333',
        'primary': '#3498db',
        'secondary': '#2c3e50',
        'success': '#27ae60',
        'danger': '#e74c3c',
        'warning': '#f39c12'
    }
}

# Business Rules
BUSINESS_RULES = {
    'default_reorder_level': 10,
    'default_location': 'Main Store',
    'password_min_length': 6
}
