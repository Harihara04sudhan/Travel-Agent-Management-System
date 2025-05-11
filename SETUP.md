# How to Run the Travel Agent Management System

Follow these steps to set up and run the Travel Agent Management System on your local machine.

## Prerequisites

Make sure you have the following installed on your system:

- Python 3.8+ (Check with `python --version` or `python3 --version`)
- pip (Python package installer)
- git (optional, for cloning the repository)

## Setup Steps

1. Clone or download the repository:
   ```
   git clone <repository-url>
   ```
   Or simply download and extract the project files.

2. Navigate to the project directory:
   ```
   cd travel-agent-management-system
   ```

3. Create and activate a virtual environment:
   
   On Windows:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Initialize the database with sample data:
   ```
   python init_db.py
   ```
   This creates a SQLite database file and populates it with sample data.

6. Start the Flask development server:
   ```
   python app.py
   ```
   Or alternatively:
   ```
   flask run
   ```

7. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Default Login Credentials

You can log in with the following credentials:

- Username: admin
- Password: admin123

## System Testing

Once logged in, you can:

1. View the dashboard with summary statistics
2. Manage travel packages
3. Add and manage customers
4. Create and manage bookings
5. Update booking statuses

## Resetting the Database

If you need to reset the database to its initial state:

1. Stop the Flask server
2. Delete the `travel_agent.db` file from the project directory
3. Run the initialization script again:
   ```
   python init_db.py
   ```
4. Restart the Flask server
