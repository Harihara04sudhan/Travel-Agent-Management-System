from app import create_app, db
from app.models import Agent, TravelPackage, Customer, Booking, Receipt
from datetime import datetime, timedelta

app = create_app()

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if we already have data
        if Agent.query.count() > 0:
            print("Database already initialized!")
            return
        
        # Create default admin user
        admin = Agent(username='admin', email='admin@travelagent.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create a demo customer user for testing
        demo_customer = Customer(
            name="Demo Customer",
            email="customer@example.com",
            phone="555-123-4567",
            address="123 Customer St, Anytown, USA",
            is_customer=True
        )
        demo_customer.set_password('customer123')
        db.session.add(demo_customer)
        
        # Create sample travel packages
        packages = [
            TravelPackage(
                name="Tropical Beach Getaway",
                description="Enjoy a relaxing week at a beautiful tropical beach resort with all-inclusive amenities.",
                destination="Bali, Indonesia",
                duration=7,
                price=1200.00,
                availability=15
            ),
            TravelPackage(
                name="European City Explorer",
                description="Visit multiple historic European cities in one amazing tour.",
                destination="Paris, Rome, Barcelona",
                duration=10,
                price=2500.00,
                availability=12
            ),
            TravelPackage(
                name="Mountain Adventure",
                description="Trek through beautiful mountain trails and stay in cozy cabins.",
                destination="Swiss Alps",
                duration=5,
                price=950.00,
                availability=20
            )
        ]
        
        for package in packages:
            db.session.add(package)
        
        # Create sample customers
        customers = [
            Customer(
                name="John Smith",
                email="john.smith@example.com",
                phone="555-123-4567",
                address="123 Main St, Anytown, USA"
            ),
            Customer(
                name="Emma Johnson",
                email="emma.johnson@example.com",
                phone="555-987-6543",
                address="456 Park Ave, Somewhere, USA"
            ),
            Customer(
                name="Michael Wong",
                email="michael.wong@example.com",
                phone="555-456-7890",
                address="789 Elm St, Nowhere, USA"
            )
        ]
        
        for customer in customers:
            db.session.add(customer)
        
        # Commit changes to create IDs
        db.session.commit()
        
        # Create sample bookings
        today = datetime.now()
        bookings = [
            Booking(
                customer_id=customers[0].id,
                package_id=packages[0].id,
                travel_date=today + timedelta(days=30),
                num_travelers=2,
                total_price=packages[0].price * 2,
                status='confirmed'
            ),
            Booking(
                customer_id=customers[1].id,
                package_id=packages[1].id,
                travel_date=today + timedelta(days=45),
                num_travelers=1,
                total_price=packages[1].price,
                status='pending'
            ),
            Booking(
                customer_id=customers[2].id,
                package_id=packages[2].id,
                travel_date=today + timedelta(days=15),
                num_travelers=4,
                total_price=packages[2].price * 4,
                status='confirmed'
            )
        ]
        
        for booking in bookings:
            db.session.add(booking)
        
        # Commit all changes
        db.session.commit()
        print("Database initialized with sample data!")

if __name__ == '__main__':
    init_db()
