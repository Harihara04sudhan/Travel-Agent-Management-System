import pytest
from app import create_app, db
from app.models import Agent, TravelPackage, Customer, Booking
from datetime import datetime, timedelta
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        
        # Create test data
        agent = Agent(username='testuser', email='test@example.com')
        agent.set_password('password')
        db.session.add(agent)
        
        package = TravelPackage(
            name="Test Package",
            description="Test Description",
            destination="Test Destination",
            duration=7,
            price=1000.00,
            availability=10
        )
        db.session.add(package)
        
        customer = Customer(
            name="Test Customer",
            email="customer@example.com",
            phone="123456789",
            address="Test Address"
        )
        db.session.add(customer)
        
        db.session.commit()
        
    yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth(client):
    return AuthActions(client)

class AuthActions:
    def __init__(self, client):
        self._client = client
    
    def login(self, username='testuser', password='password'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Travel Agent Management System' in response.data

def test_login(client, auth):
    response = auth.login()
    assert response.headers['Location'] == '/dashboard'
    
    with client:
        client.get('/')
        assert client.get('/dashboard').status_code == 200

def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        response = client.get('/dashboard')
        assert response.headers['Location'].startswith('/auth/login')

def test_package_listing(client, auth, app):
    auth.login()
    response = client.get('/packages/')
    assert response.status_code == 200
    assert b'Test Package' in response.data

def test_customer_listing(client, auth, app):
    auth.login()
    response = client.get('/customers/')
    assert response.status_code == 200
    assert b'Test Customer' in response.data

def test_create_booking(client, auth, app):
    auth.login()
    
    with app.app_context():
        customer = Customer.query.first()
        package = TravelPackage.query.first()
        
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        response = client.post('/bookings/create', data={
            'customer_id': customer.id,
            'package_id': package.id,
            'travel_date': tomorrow,
            'num_travelers': 2
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Booking created successfully!' in response.data
        
        booking = Booking.query.first()
        assert booking is not None
        assert booking.customer_id == customer.id
        assert booking.package_id == package.id
        assert booking.num_travelers == 2

def test_duplicate_customer_registration(test_client, init_database):
    # First registration
    response = test_client.post('/register', data={
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '1234567890',
        'password': 'password123'
    }, follow_redirects=True)
    assert b'Registration successful!' in response.data
    
    # Try registering with same email
    response = test_client.post('/register', data={
        'name': 'Jane Doe',
        'email': 'john@example.com',  # Same email
        'phone': '0987654321',
        'password': 'password123'
    }, follow_redirects=True)
    assert b'A customer with this email already exists!' in response.data
    
    # Try registering with same phone
    response = test_client.post('/register', data={
        'name': 'Jane Doe',
        'email': 'jane@example.com',
        'phone': '1234567890',  # Same phone
        'password': 'password123'
    }, follow_redirects=True)
    assert b'A customer with this phone already exists!' in response.data
