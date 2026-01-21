# SyncBazar - Inventory Management System

A comprehensive desktop-based inventory management system built with Python Tkinter and SQL Server.

## Features

- 🔐 **User Authentication** - Secure login with role-based access
- 📦 **Smart Inventory Management** - Add, edit, delete, and search items
- 🏪 **Shop Network** - Manage multiple store locations
- 🔍 **Network Search** - Search items across all connected stores
- 📊 **Real-time Analysis** - Dashboard with statistics and reports
- 💾 **SQL Server Database** - Reliable data storage and management

## Technology Stack

- **Frontend:** Python Tkinter (GUI)
- **Backend:** Python 3.8+
- **Database:** Microsoft SQL Server
- **Database Connector:** pyodbc

## Installation

### Prerequisites

1. **Python 3.8 or higher**
2. **Microsoft SQL Server** (Express edition works fine)
3. **ODBC Driver 17 for SQL Server**

### Setup Steps

1. **Clone or download the project**
   ```bash
   git clone [repository-url]
   cd SyncBazar
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up SQL Server Database**
   - Ensure your SQL Server has the `Bazar_db` database created and running.

4. **Configure database connection**
   - Edit `config.py` if needed (default uses Windows Authentication)

5. **Run the application**
   ```bash
   python main.py
   ```

## Default Login Credentials

- **Username:** `admin`
- **Password:** `admin123`

## Project Structure

```
SyncBazar/
├── database/          # Database connection and queries
├── views/            # Tkinter windows and UI
├── controllers/      # Business logic
├── utils/           # Utilities and helpers
├── tests/           # Unit tests
├── config.py        # Configuration
├── main.py          # Application entry point
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Modules

### 1. Login Window
- Secure user authentication
- Remember me functionality
- Error handling for invalid credentials

### 2. Dashboard
- System overview with statistics
- Quick access to all features
- Recent activity log

### 3. Inventory Management
- Complete CRUD operations for items
- Stock level tracking
- Low stock alerts
- Search and filter functionality

### 4. Shop Network
- Manage multiple store locations
- Store details and status
- Location-based organization

### 5. Network Search
- Search items across all stores
- Real-time availability check
- Filter by various criteria

### 6. Real-time Analysis
- System statistics and metrics
- Inventory analysis reports
- Business intelligence

## Database Schema

### Main Tables:
1. **users** - User accounts and authentication
2. **items** - Product inventory
3. **shops** - Store locations
4. **activity_log** - System activity tracking

## Features in Detail

### User Management
- Role-based access control (Admin/Staff)
- Secure password storage
- User activity logging

### Inventory Features
- Product categorization
- SKU/Barcode management
- Stock level monitoring
- Automatic reorder alerts
- Supplier management

### Multi-store Support
- Centralized inventory management
- Store-specific stock levels
- Location-based organization
- Inter-store transfers

### Reporting & Analytics
- Real-time dashboard
- Sales and stock reports
- Performance metrics
- Data export capability

## Troubleshooting

### Common Issues:

1. **Database Connection Failed**
   - Check SQL Server is running
   - Verify server name in config.py
   - Ensure ODBC Driver 17 is installed

2. **Import Errors**
   - Make sure all dependencies are installed
   - Check Python version (3.8+ required)

3. **Login Issues**
   - Verify database has been created with SCD(Tkinter).sql
   - Check default credentials

### Logs:
- Application logs errors to console
- Database errors are displayed in message boxes
- Activity is logged in the database

## Development

### Running Tests
```bash
python -m unittest tests/test_database.py
```

### Code Style
- Follows PEP 8 guidelines
- Meaningful variable names
- Comprehensive comments

### Version Control
- Uses Git for source control
- Feature branch workflow recommended

## License

This project is developed for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the documentation
3. Contact the development team

---

**SyncBazar - Transforming Retail Inventory Management**
