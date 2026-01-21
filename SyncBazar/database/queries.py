"""
SQL queries for SyncBazar
"""

# User queries
CREATE_USERS_TABLE = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    email VARCHAR(100),
    role VARCHAR(50) DEFAULT 'staff',
    created_at DATETIME DEFAULT GETDATE(),
    is_active BIT DEFAULT 1
)
"""

INSERT_DEFAULT_USER = """
INSERT INTO users (username, password, full_name, email, role)
VALUES ('admin', 'admin123', 'Administrator', 'admin@syncbazar.com', 'admin')
"""

CHECK_LOGIN = """
SELECT user_id, username, full_name, role 
FROM users 
WHERE username = ? AND password = ? AND is_active = 1
"""

# Item queries
CREATE_ITEMS_TABLE = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='items' AND xtype='U')
CREATE TABLE items (
    item_id INT IDENTITY(1,1) PRIMARY KEY,
    item_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    sku VARCHAR(50) UNIQUE,
    quantity INT NOT NULL DEFAULT 0,
    reorder_level INT DEFAULT 10,
    unit_price DECIMAL(10,2) NOT NULL,
    location VARCHAR(100),
    supplier VARCHAR(200),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
)
"""

INSERT_SAMPLE_ITEMS = """
INSERT INTO items (item_name, category, sku, quantity, unit_price, location, supplier)
VALUES 
('Laptop Pro', 'Electronics', 'ELEC-001', 50, 1200.00, 'Warehouse A', 'Dell Inc.'),
('Wireless Mouse', 'Electronics', 'ELEC-002', 200, 25.99, 'Main Store', 'Logitech'),
('Office Chair', 'Furniture', 'FURN-001', 75, 199.99, 'Warehouse A', 'IKEA'),
('Notebook', 'Stationery', 'STAT-001', 500, 4.50, 'Warehouse B', 'Stationery Co.')
"""

GET_ALL_ITEMS = """
SELECT item_id, item_name, category, sku, quantity, 
       reorder_level, unit_price, location, supplier, created_at
FROM items 
ORDER BY item_name
"""

ADD_ITEM = """
INSERT INTO items (item_name, category, sku, quantity, reorder_level, unit_price, location, supplier)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

UPDATE_ITEM = """
UPDATE items 
SET item_name = ?, category = ?, sku = ?, quantity = ?,
    reorder_level = ?, unit_price = ?, location = ?, supplier = ?,
    updated_at = GETDATE()
WHERE item_id = ?
"""

DELETE_ITEM = "DELETE FROM items WHERE item_id = ?"

SEARCH_ITEMS = """
SELECT item_id, item_name, category, sku, quantity, unit_price, location, supplier
FROM items 
WHERE item_name LIKE ? OR category LIKE ? OR sku LIKE ? OR supplier LIKE ?
ORDER BY item_name
"""

# Shop queries
CREATE_SHOPS_TABLE = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='shops' AND xtype='U')
CREATE TABLE shops (
    shop_id INT IDENTITY(1,1) PRIMARY KEY,
    shop_name VARCHAR(200) NOT NULL,
    location VARCHAR(300),
    manager_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    status VARCHAR(20) DEFAULT 'Active',
    created_at DATETIME DEFAULT GETDATE()
)
"""

INSERT_SAMPLE_SHOPS = """
INSERT INTO shops (shop_name, location, manager_name, phone, email)
VALUES 
('Main Store', '123 Main Street, Karachi', 'Ahmed Khan', '0300-1234567', 'main@syncbazar.com'),
('Branch A', '456 Gulshan, Lahore', 'Ali Raza', '0300-7654321', 'branch.a@syncbazar.com'),
('Warehouse', '789 Industrial Area, Islamabad', 'Usman Ahmed', '0300-9876543', 'warehouse@syncbazar.com')
"""

GET_ALL_SHOPS = """
SELECT shop_id, shop_name, location, manager_name, phone, email, status
FROM shops 
ORDER BY shop_name
"""

# Activity log
CREATE_ACTIVITY_TABLE = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='activity_log' AND xtype='U')
CREATE TABLE activity_log (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    activity_type VARCHAR(50),
    description VARCHAR(500),
    item_id INT,
    quantity_changed INT,
    user_id INT,
    created_at DATETIME DEFAULT GETDATE()
)
"""

# Dashboard queries
GET_DASHBOARD_STATS = """
SELECT 
    (SELECT COUNT(*) FROM items) as total_items,
    (SELECT COUNT(*) FROM shops) as total_shops,
    (SELECT SUM(quantity * unit_price) FROM items) as total_value,
    (SELECT COUNT(*) FROM items WHERE quantity < reorder_level AND quantity > 0) as low_stock,
    (SELECT COUNT(*) FROM items WHERE quantity = 0) as out_of_stock
"""

GET_RECENT_ACTIVITY = """
SELECT TOP 5 description, created_at 
FROM activity_log 
ORDER BY created_at DESC
"""
