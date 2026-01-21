"""
Authentication controller
"""
from database.connection import db
from database.queries import CHECK_LOGIN


class AuthController:
    """Handles authentication logic"""
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user"""
        if not username or not password:
            return None, "Username and password are required"
        
        result = db.fetch_one(CHECK_LOGIN, (username, password))
        
        if result:
            user_id, username, full_name, role = result
            return {
                'user_id': user_id,
                'username': username,
                'full_name': full_name,
                'role': role
            }, None
        else:
            return None, "Invalid username or password"
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        return True, ""
