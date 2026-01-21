"""
Database connection module for SQL Server
"""
import pyodbc
from config import DB_CONFIG


class DatabaseConnection:
    """Handles SQL Server database connection"""
    
    def __init__(self):
        self.server = DB_CONFIG['server']
        self.database = DB_CONFIG['database']
        self.username = DB_CONFIG['username']
        self.password = DB_CONFIG['password']
        self.driver = DB_CONFIG['driver']
        self.trusted_connection = DB_CONFIG.get('trusted_connection', 'yes')
        self.conn = None
    
    def connect(self):
        """Establish connection to SQL Server"""
        try:
            if self.trusted_connection.lower() == 'yes':
                conn_str = (
                    f'DRIVER={{{self.driver}}};'
                    f'SERVER={self.server};'
                    f'DATABASE={self.database};'
                    f'Trusted_Connection=yes;'
                )
            else:
                conn_str = (
                    f'DRIVER={{{self.driver}}};'
                    f'SERVER={self.server};'
                    f'DATABASE={self.database};'
                    f'UID={self.username};'
                    f'PWD={self.password}'
                )
            
            self.conn = pyodbc.connect(conn_str)
            self.conn.autocommit = True
            print("✅ Database connected successfully")
            return True
        except pyodbc.Error as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def execute_query(self, query, params=None):
        """Execute SQL query"""
        # [SW Engineering] Exception Handling: Applies strict try-except blocks to manage database errors
        # gracefully without crashing the application. Logs errors for debugging.
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except pyodbc.Error as e:
            print(f"❌ Query execution failed: {e}")
            return None
    
    def fetch_all(self, query, params=None):
        """Fetch all results"""
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchall()
        return []
    
    def fetch_one(self, query, params=None):
        """Fetch single result"""
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchone()
        return None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed")


# Global database instance
db = DatabaseConnection()
