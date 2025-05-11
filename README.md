# Travel Agent Management System

A comprehensive web-based system for travel agencies to manage customers, travel packages, and bookings. Built with Flask and SQLite for easy local development.

## Features

- **Customer Management**: Store and manage customer details
- **Travel Package Management**: Create and manage travel packages with destinations, prices, etc.
- **Booking System**: Create bookings linking customers to packages
- **Admin Dashboard**: Overview of agency operations with key statistics
- **Authentication**: Secure login for both admins and customers
- **Customer Portal**: Allow customers to register, browse packages, and make bookings
- **Professional Receipts**: Generate detailed receipts for customer bookings

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.8+ 
- Pip (Python package installer)
- Git

### Installation

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd travel-agent-management-system
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/macOS
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database
   ```bash
   python init_db.py
   ```

5. Run the application
   ```bash
   flask run
   # Or
   python app.py
   ```

6. Access the application in your web browser at `http://127.0.0.1:5000/`

### Default Logins

#### Admin Login
- Username: admin
- Password: admin123

#### Customer Demo Login
- Email: customer@example.com
- Password: customer123

## Project Structure

```
travel-agent-management-system/
├── app/                    # Application package
│   ├── __init__.py         # App factory and extensions
│   ├── models.py           # Database models
│   ├── routes.py           # Application routes
│   ├── static/             # Static assets (CSS, JS)
│   └── templates/          # HTML templates
├── tests/                  # Test suite
├── app.py                  # Application entry point
├── config.py               # Configuration settings
├── init_db.py              # Database initialization script
└── requirements.txt        # Project dependencies
```

## Testing

Run the test suite with pytest:

```bash
pytest
```

## Built With

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Flask-Login](https://flask-login.readthedocs.io/) - User session management

## License

This project is open source and available under the [MIT License](LICENSE).

## Troubleshooting

### SQLAlchemy Compatibility Issues

If you encounter SQLAlchemy-related errors, ensure you're using a compatible version:

```bash
# Fix for SQLAlchemy compatibility issues
pip install "sqlalchemy<2.0.0"
```

This project is configured to work with SQLAlchemy 1.x. The requirements.txt file has been updated to include this constraint.

### Running Tests

A testing script is included to help diagnose common issues:

```bash
./test_setup.sh
```

For more information about testing, please see [TESTING.md](TESTING.md).
