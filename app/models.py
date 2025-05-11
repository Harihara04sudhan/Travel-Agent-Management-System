from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import random

@login_manager.user_loader
def load_user(id):
    # Try to load as an agent first
    user = Agent.query.get(int(id))
    if user:
        return user
    # If not an agent, try as a customer
    return Customer.query.get(int(id))

class Agent(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=True)  # To distinguish from customers
    
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

class Customer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    is_customer = db.Column(db.Boolean, default=True)  # To distinguish from agents
    
    # Relationships
    bookings = db.relationship('Booking', backref='customer', lazy=True)
    
    def __repr__(self):
        return f'<Customer {self.name}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def check_existing_customer(cls, email=None, phone=None):
        """Check if a customer already exists with given email or phone"""
        if email:
            existing_email = cls.query.filter_by(email=email).first()
            if existing_email:
                return {'exists': True, 'field': 'email'}
        
        if phone:
            existing_phone = cls.query.filter_by(phone=phone).first()
            if existing_phone:
                return {'exists': True, 'field': 'phone'}
        
        return {'exists': False}

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
    
    def calculate_total_price(self):
        if self.package and self.num_travelers:
            return self.package.price * self.num_travelers
        return 0

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    receipt_number = db.Column(db.String(20), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), nullable=False, default='PENDING')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with Booking
    booking = db.relationship('Booking', backref=db.backref('receipt', uselist=False, single_parent=True), 
                            single_parent=True)

    def __init__(self, **kwargs):
        booking = kwargs.get('booking')
        if booking:
            self.booking = booking
            self.booking_id = booking.id
            self.amount = booking.total_price
        else:
            self.booking_id = kwargs.get('booking_id')
            self.amount = kwargs.get('final_amount', 0)
            
        self.payment_method = kwargs.get('payment_method', 'Credit Card')
        self.receipt_number = f"RCPT-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000,9999)}"
        self.payment_status = kwargs.get('payment_status', 'PAID')

    def to_dict(self):
        return {
            'receipt_number': self.receipt_number,
            'booking_id': self.booking_id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
