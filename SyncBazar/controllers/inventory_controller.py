"""
Inventory controller
"""
from database.connection import db
from database.queries import ADD_ITEM, UPDATE_ITEM, DELETE_ITEM
from utils.validators import validate_numeric


class InventoryController:
    """Handles inventory business logic"""
    
    @staticmethod
    def add_item(item_data):
        """
        Add new item
        
        [SW Engineering] Refactoring & Lehman's Law:
        - Logic is encapsulated in this Controller (MVC Pattern) rather than the View.
        - This separation makes it easier to 'Refactor' and 'Remove Legacy Code' without breaking the UI.
        - As per Lehman's Law (Continuing Change), this modularity allows the system to evolve easily
          as user requirements change over time.
        """
        # Validate required fields
        if not item_data.get('name'):
            return False, "Item name is required"
        
        # Validate numeric fields
        quantity_valid, quantity_msg = validate_numeric(item_data.get('quantity', 0), "Quantity")
        if not quantity_valid:
            return False, quantity_msg
        
        price_valid, price_msg = validate_numeric(item_data.get('price', 0), "Price")
        if not price_valid:
            return False, price_msg
        
        try:
            # Add to database
            db.execute_query(ADD_ITEM, (
                item_data['name'],
                item_data.get('category', 'General'),
                item_data.get('sku', ''),
                int(float(item_data['quantity'])),
                10,  # Default reorder level
                float(item_data['price']),
                item_data.get('location', 'Main Store'),
                item_data.get('supplier', '')
            ))
            return True, "Item added successfully"
        except Exception as e:
            return False, f"Failed to add item: {str(e)}"
    
    @staticmethod
    def update_item(item_id, item_data):
        """Update existing item"""
        if not item_data.get('name'):
            return False, "Item name is required"
        
        quantity_valid, quantity_msg = validate_numeric(item_data.get('quantity', 0), "Quantity")
        if not quantity_valid:
            return False, quantity_msg
        
        price_valid, price_msg = validate_numeric(item_data.get('price', 0), "Price")
        if not price_valid:
            return False, price_msg
        
        try:
            db.execute_query(UPDATE_ITEM, (
                item_data['name'],
                item_data.get('category', 'General'),
                item_data.get('sku', ''),
                int(float(item_data['quantity'])),
                10,
                float(item_data['price']),
                item_data.get('location', 'Main Store'),
                item_data.get('supplier', ''),
                item_id
            ))
            return True, "Item updated successfully"
        except Exception as e:
            return False, f"Failed to update item: {str(e)}"
    
    @staticmethod
    def delete_item(item_id):
        """Delete item"""
        try:
            db.execute_query(DELETE_ITEM, (item_id,))
            return True, "Item deleted successfully"
        except Exception as e:
            return False, f"Failed to delete item: {str(e)}"
