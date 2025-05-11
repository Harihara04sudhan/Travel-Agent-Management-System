"""
Update database schema for user login and receipt functionality

This script updates the database schema to add:
1. Password field to Customer model
2. is_customer field to Customer model
3. is_admin field to Agent model
4. Receipt model and relationship with Booking
"""

from app import create_app, db
from app.models import Agent, Customer, Booking, Receipt, TravelPackage
import sqlalchemy as sa
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

def upgrade_database():
    """Upgrade database schema with new columns and tables"""
    
    with app.app_context():
        # Create a session
        session = db.session
        connection = session.connection()
        
        # Check if we need to add password_hash to Customer
        inspector = sa.inspect(connection)
        customer_columns = [col['name'] for col in inspector.get_columns('customer')]
        
        if 'password_hash' not in customer_columns:
            print("Adding password_hash column to Customer table")
            connection.execute(sa.text(
                "ALTER TABLE customer ADD COLUMN password_hash VARCHAR(128)"
            ))
        
        if 'is_customer' not in customer_columns:
            print("Adding is_customer column to Customer table")
            connection.execute(sa.text(
                "ALTER TABLE customer ADD COLUMN is_customer BOOLEAN DEFAULT TRUE"
            ))
        
        # Check if we need to add is_admin to Agent
        agent_columns = [col['name'] for col in inspector.get_columns('agent')]
        
        if 'is_admin' not in agent_columns:
            print("Adding is_admin column to Agent table")
            connection.execute(sa.text(
                "ALTER TABLE agent ADD COLUMN is_admin BOOLEAN DEFAULT TRUE"
            ))
        
        # Check if Receipt table exists
        receipt_exists = 'receipt' in inspector.get_table_names()
        
        if not receipt_exists:
            print("Creating Receipt table")
            # First drop any foreign keys that might conflict
            # Create the Receipt table
            connection.execute(sa.text("""
                CREATE TABLE receipt (
                    id INTEGER NOT NULL, 
                    booking_id INTEGER NOT NULL, 
                    receipt_number VARCHAR(50) NOT NULL, 
                    issue_date DATETIME, 
                    payment_method VARCHAR(50), 
                    tax_amount FLOAT DEFAULT 0.0, 
                    discount_amount FLOAT DEFAULT 0.0, 
                    final_amount FLOAT NOT NULL, 
                    PRIMARY KEY (id), 
                    UNIQUE (booking_id), 
                    UNIQUE (receipt_number), 
                    FOREIGN KEY(booking_id) REFERENCES booking (id)
                )
            """))
        
        # Commit the changes
        session.commit()
        print("Database schema update completed successfully")
        
        # Set default passwords for existing customers
        customers = Customer.query.all()
        for customer in customers:
            if not customer.password_hash:
                print(f"Setting default password for customer: {customer.name}")
                customer.password_hash = generate_password_hash('password123')
        
        session.commit()
        print("Default passwords set for existing customers")

if __name__ == "__main__":
    upgrade_database()
