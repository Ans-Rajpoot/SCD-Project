"""
Unit tests for database operations 
"""
import unittest
from database.connection import DatabaseConnection

class TestDatabase(unittest.TestCase):
    """
    Test database connection and operations
    
    [SW Engineering] Automated Testing:
    - This class implements Unit Testing using Python's 'unittest' framework.
    - It allows for automated verification of database connectivity and query execution.
    - Supports Regression Testing to ensure new changes (refactoring) don't break existing features.
    """
    
    def setUp(self):
        """Set up test database connection"""
        self.db = DatabaseConnection()
    
    def test_connection(self):
        """Test database connection"""
        result = self.db.connect()
        self.assertTrue(result, "Database should connect successfully")
    
    def test_execute_query(self):
        """Test query execution"""
        self.db.connect()
        cursor = self.db.execute_query("SELECT 1 as test")
        self.assertIsNotNone(cursor, "Query should execute successfully")
    
    def test_fetch_all(self):
        """Test fetch all results"""
        self.db.connect()
        results = self.db.fetch_all("SELECT 1 as num UNION SELECT 2")
        self.assertEqual(len(results), 2, "Should fetch 2 rows")
    
    def test_fetch_one(self):
        """Test fetch single result"""
        self.db.connect()
        result = self.db.fetch_one("SELECT 42 as answer")
        self.assertIsNotNone(result, "Should fetch one row")
        self.assertEqual(result[0], 42, "Should return correct value")


if __name__ == '__main__':
    unittest.main()
