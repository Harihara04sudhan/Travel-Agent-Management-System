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

- Python 3.8+ (python3 command)
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
   # Ensure you are in the travel-agent-management-system directory
   python3 -m venv oose  # Or your preferred name e.g., venv
   
   # On Windows
   oose\Scripts\activate
   
   # On Linux/macOS
   source oose/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database
   ```bash
   python3 init_db.py
   ```

5. Run the application
   ```bash
   # Ensure your FLASK_APP environment variable is set.
   # If your main app is in the 'app' package (e.g., app/__init__.py creates the Flask app instance):
   # On Linux/macOS:
   # export FLASK_APP=app
   # On Windows (Command Prompt):
   # set FLASK_APP=app
   # On Windows (PowerShell):
   # $env:FLASK_APP="app"
   #
   # If app/__init__.py uses an app factory like create_app(), you might use:
   # export FLASK_APP="app:create_app()" (adjust for your OS)

   flask run
   ```

6. Access the application in your web browser at `http://120.0.1:5000/`

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
│   ├── __init__.py         # App factory and Flask app instance
│   ├── models.py           # Database models (SQLAlchemy)
│   ├── routes.py           # Application routes and view functions
│   ├── static/             # Static assets
│   │   ├── css/
│   │   │   └── style.css   # Main stylesheet
│   │   └── js/
│   │       ├── script.js   # General JavaScript (if any)
│   │       └── validation.js # Form validation JavaScript
│   └── templates/          # HTML templates (Jinja2)
│       ├── base.html       # Base template for layout
│       ├── index.html      # Homepage template
│       ├── login.html      # Login and registration page
│       ├── dashboard.html  # Admin dashboard
│       ├── auth/
│       │   └── register.html # Customer registration specific template (if separate)
│       ├── packages/       # Admin package management templates
│       │   ├── list.html
│       │   ├── create.html
│       │   └── ...
│       ├── user/           # Customer-facing templates
│       │   ├── dashboard.html
│       │   ├── packages.html
│       │   ├── receipt.html
│       │   └── ...
│       └── ...             # Other templates for bookings, customers etc.
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py         # Pytest configuration and fixtures
│   └── test_app.py         # Application tests
├── config.py               # Configuration settings (e.g., database URI)
├── init_db.py              # Database initialization script
├── requirements.txt        # Project dependencies
├── .gitignore              # Specifies intentionally untracked files that Git should ignore
└── README.md               # This file
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

## Contributing & Feedback

We welcome contributions and feedback! If you encounter any issues, have suggestions for improvements, or would like to contribute to the project, please feel free to:

- **Open an Issue**: Report bugs or suggest features on the [GitHub Issues page](https://github.com/Harihara04sudhan/oose/issues).
- **Submit a Pull Request**: If you'd like to contribute code, please fork the repository and submit a pull request with your changes.

Your input is valuable in making this project better!

## License

This project is open source and available under the [MIT License](LICENSE).
