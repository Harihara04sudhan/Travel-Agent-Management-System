# Travel Agent Management System Implementation Plan

This document outlines how to run the Travel Agent Management System which has been implemented using Flask, SQLite, and the Python ecosystem.

## System Overview

The Travel Agent Management System has been implemented with the following features:

1. Agent Authentication (Login/Logout)
2. Travel Package Management (View, Create, Details)
3. Customer Management
4. Booking Management
5. Dashboard with Statistics

## Running the Application

There are two ways to run the application:

### Method 1: Full Application Structure

The application can be run with full modular structure:

```bash
# Navigate to project directory
cd "/home/harisudhan/Pictures/oose/travel mangemnet system/travel-agent-management-system/"

# Activate virtual environment
source oose/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py  

# Run the application
python app.py
```

### Method 2: Simple Single-File Application

For a quick start and demonstration, a simplified version with all functionality in a single file is provided:

```bash
# Navigate to project directory
cd "/home/harisudhan/Pictures/oose/travel mangemnet system/travel-agent-management-system/"

# Activate virtual environment
source oose/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the simple application
python simple_app.py
```

## Accessing the Application

Once the application is running, you can access it in your browser at:
```
http://127.0.0.1:5000/
```

### Default Login Credentials
- Username: admin
- Password: admin123

## Application Structure

The full application follows a modular structure:

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

While the repository includes a basic test suite, the focus of this implementation was on functionality for demonstration purposes.
