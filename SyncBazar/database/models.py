"""
Data models for SyncBazar
"""

class User:
    def __init__(self, user_id, username, full_name, role):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.role = role
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'full_name': self.full_name,
            'role': self.role
        }


class Item:
    def __init__(self, item_id, item_name, category, sku, quantity, 
                 reorder_level, unit_price, location, supplier, created_at=None):
        self.item_id = item_id
        self.item_name = item_name
        self.category = category
        self.sku = sku
        self.quantity = quantity
        self.reorder_level = reorder_level
        self.unit_price = unit_price
        self.location = location
        self.supplier = supplier
        self.created_at = created_at
    
    def to_dict(self):
        return {
            'item_id': self.item_id,
            'item_name': self.item_name,
            'category': self.category,
            'sku': self.sku,
            'quantity': self.quantity,
            'reorder_level': self.reorder_level,
            'unit_price': float(self.unit_price),
            'location': self.location,
            'supplier': self.supplier,
            'total_value': self.quantity * float(self.unit_price)
        }
    
    def get_status(self):
        if self.quantity == 0:
            return "Out of Stock"
        elif self.quantity < self.reorder_level:
            return "Low Stock"
        else:
            return "In Stock"


class Shop:
    def __init__(self, shop_id, shop_name, location, manager_name, 
                 phone, email, status):
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.location = location
        self.manager_name = manager_name
        self.phone = phone
        self.email = email
        self.status = status
    
    def to_dict(self):
        return {
            'shop_id': self.shop_id,
            'shop_name': self.shop_name,
            'location': self.location,
            'manager_name': self.manager_name,
            'phone': self.phone,
            'email': self.email,
            'status': self.status
        }
