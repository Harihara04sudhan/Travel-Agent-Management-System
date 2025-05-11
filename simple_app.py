from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
import sqlalchemy

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_agent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database without relying on __all__ attribute
db = SQLAlchemy()

# Define models
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    def __repr__(self):
        return f'<Agent {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class TravelPackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    destination = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in days
    price = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Integer, default=10)  # max number of bookings
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='package', lazy=True)
    
    def __repr__(self):
        return f'<Package {self.name} - {self.destination}>'

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='customer', lazy=True)
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('travel_package.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    travel_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    num_travelers = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Float)
    
    def __repr__(self):
        return f'<Booking #{self.id} - {self.status}>'

# Routes
@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        agent = Agent.query.filter_by(username=username).first()
        
        if agent is None or not agent.check_password(password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        
        session['user_id'] = agent.id
        session['username'] = agent.username
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', title='Sign In')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    packages_count = TravelPackage.query.count()
    customers_count = Customer.query.count()
    bookings_count = Booking.query.count()
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                          title='Dashboard',
                          packages_count=packages_count,
                          customers_count=customers_count,
                          bookings_count=bookings_count,
                          recent_bookings=recent_bookings)

# Package routes
@app.route('/packages')
def list_packages():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    packages = TravelPackage.query.all()
    return render_template('packages/list.html', title='Travel Packages', packages=packages)

@app.route('/packages/create', methods=['GET', 'POST'])
def create_package():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        package = TravelPackage(
            name=request.form.get('name'),
            description=request.form.get('description'),
            destination=request.form.get('destination'),
            duration=int(request.form.get('duration')),
            price=float(request.form.get('price')),
            availability=int(request.form.get('availability'))
        )
        
        db.session.add(package)
        db.session.commit()
        flash('Package created successfully!', 'success')
        return redirect(url_for('list_packages'))
    
    return render_template('packages/create.html', title='Create Package')

@app.route('/packages/<int:id>')
def view_package(id):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    package = TravelPackage.query.get_or_404(id)
    return render_template('packages/view.html', title=package.name, package=package)

# Initialize the database
def init_db():
    # Create tables
    db.create_all()
    
    # Check if we already have data
    if Agent.query.count() > 0:
        print("Database already initialized!")
        return
    
    # Create default admin user
    admin = Agent(username='admin', email='admin@travelagent.com')
    admin.set_password('admin123')
    db.session.add(admin)
        
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

def init_app():
    db.init_app(app)
    
    with app.app_context():
        # Initialize the database if it doesn't exist
        db_path = os.path.join(os.path.dirname(__file__), 'travel_agent.db')
        if not os.path.exists(db_path):
            init_db()

if __name__ == '__main__':
    # Initialize the app with the database
    init_app()
    
    # Run the app
    app.run(debug=True)
