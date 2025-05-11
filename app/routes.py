from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Agent, TravelPackage, Customer, Booking, Receipt
from werkzeug.urls import url_parse
from datetime import datetime
import secrets
import string

# Blueprint definitions
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
package_bp = Blueprint('package', __name__)
customer_bp = Blueprint('customer', __name__)
booking_bp = Blueprint('booking', __name__)
user_bp = Blueprint('user', __name__)

# Main routes
@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@main_bp.route('/dashboard')
@login_required
def dashboard():
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

# Authentication routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirect to appropriate dashboard based on user type
        if hasattr(current_user, 'is_admin') and current_user.is_admin:
            return redirect(url_for('main.dashboard'))
        else:
            return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username') # For customers, this should be their email
        password = request.form.get('password')
        remember = 'remember' in request.form
        user_type = request.form.get('user_type', 'customer') # Default to customer if not specified
        
        user = None
        if user_type == 'admin':
            user = Agent.query.filter_by(username=username).first()
        else: # Assumes 'customer'
            user = Customer.query.filter_by(email=username).first()
            
        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=remember)
        
        # Set user type in session for later use, if needed, though Flask-Login's current_user should suffice
        session['user_type'] = 'admin' if hasattr(user, 'is_admin') and user.is_admin else 'customer'
        
        # Redirect to appropriate dashboard
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            if session['user_type'] == 'admin':
                next_page = url_for('main.dashboard')
            else:
                next_page = url_for('user.dashboard')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Check if customer already exists
        existing = Customer.check_existing_customer(email=email, phone=phone)
        if existing['exists']:
            field = existing['field']
            flash(f'A customer with this {field} already exists!', 'error')
            return redirect(url_for('auth.register'))
        
        # Continue with registration if customer doesn't exist
        customer = Customer(
            name=request.form.get('name'),
            email=email,
            phone=phone
        )
        customer.set_password(request.form.get('password'))
        
        db.session.add(customer)
        try:
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration.', 'error')
            return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html')

@auth_bp.route('/api/check-customer')
def check_customer():
    email = request.args.get('email')
    phone = request.args.get('phone')
    
    result = Customer.check_existing_customer(email=email, phone=phone)
    return jsonify(result)

# Package routes
@package_bp.route('/')
@login_required
def list_packages():
    packages = TravelPackage.query.all()
    return render_template('packages/list.html', title='Travel Packages', packages=packages)

@package_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_package():
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
        return redirect(url_for('package.list_packages'))
    
    return render_template('packages/create.html', title='Create Package')

@package_bp.route('/<int:id>')
@login_required
def view_package(id):
    package = TravelPackage.query.get_or_404(id)
    return render_template('packages/view.html', title=package.name, package=package)

@package_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_package(id):
    package = TravelPackage.query.get_or_404(id)
    
    if request.method == 'POST':
        package.name = request.form.get('name')
        package.description = request.form.get('description')
        package.destination = request.form.get('destination')
        package.duration = int(request.form.get('duration'))
        package.price = float(request.form.get('price'))
        package.availability = int(request.form.get('availability'))
        
        db.session.commit()
        flash('Package updated successfully!', 'success')
        return redirect(url_for('package.view_package', id=package.id))
    
    return render_template('packages/edit.html', title=f'Edit {package.name}', package=package)

@package_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_package(id):
    package = TravelPackage.query.get_or_404(id)
    db.session.delete(package)
    db.session.commit()
    flash('Package deleted successfully!', 'success')
    return redirect(url_for('package.list_packages'))

# Customer routes
@customer_bp.route('/')
@login_required
def list_customers():
    customers = Customer.query.all()
    return render_template('customers/list.html', title='Customers', customers=customers)

@customer_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_customer():
    if request.method == 'POST':
        customer = Customer(
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            address=request.form.get('address')
        )
        
        db.session.add(customer)
        db.session.commit()
        flash('Customer created successfully!', 'success')
        return redirect(url_for('customer.list_customers'))
    
    return render_template('customers/create.html', title='Create Customer')

@customer_bp.route('/<int:id>')
@login_required
def view_customer(id):
    customer = Customer.query.get_or_404(id)
    return render_template('customers/view.html', title=customer.name, customer=customer)

@customer_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.email = request.form.get('email')
        customer.phone = request.form.get('phone')
        customer.address = request.form.get('address')
        
        db.session.commit()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customer.view_customer', id=customer.id))
    
    return render_template('customers/edit.html', title=f'Edit {customer.name}', customer=customer)

@customer_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('customer.list_customers'))

# Booking routes
@booking_bp.route('/')
@login_required
def list_bookings():
    bookings = Booking.query.all()
    return render_template('bookings/list.html', title='Bookings', bookings=bookings)

@booking_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_booking():
    packages = TravelPackage.query.all()
    customers = Customer.query.all()
    
    if request.method == 'POST':
        customer_id = int(request.form.get('customer_id'))
        package_id = int(request.form.get('package_id'))
        travel_date_str = request.form.get('travel_date')
        num_travelers = int(request.form.get('num_travelers'))
        
        # Parse travel date
        travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d')
        
        # Get package to calculate price
        package = TravelPackage.query.get(package_id)
        
        booking = Booking(
            customer_id=customer_id,
            package_id=package_id,
            travel_date=travel_date,
            num_travelers=num_travelers,
            total_price=package.price * num_travelers,
            status='pending'
        )
        
        db.session.add(booking)
        db.session.commit()
        flash('Booking created successfully!', 'success')
        return redirect(url_for('booking.list_bookings'))
    
    return render_template('bookings/create.html', 
                          title='Create Booking',
                          packages=packages,
                          customers=customers)

@booking_bp.route('/<int:id>')
@login_required
def view_booking(id):
    booking = Booking.query.get_or_404(id)
    return render_template('bookings/view.html', title=f'Booking #{booking.id}', booking=booking)

@booking_bp.route('/<int:id>/status', methods=['POST'])
@login_required
def update_booking_status(id):
    booking = Booking.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'confirmed', 'cancelled']:
        booking.status = new_status
        db.session.commit()
        flash(f'Booking status updated to {new_status}!', 'success')
    else:
        flash('Invalid status!', 'danger')
    
    return redirect(url_for('booking.view_booking', id=booking.id))

@booking_bp.route('/receipt/<int:booking_id>')
@login_required
def view_receipt(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if receipt exists, if not create one
    if not hasattr(booking, 'receipt'):
        receipt = Receipt(booking=booking, payment_method='Credit Card')
        db.session.add(receipt)
        db.session.commit()
    
    return render_template('booking/receipt.html', 
                         booking=booking, 
                         receipt=booking.receipt)

@booking_bp.route('/generate_receipt/<int:booking_id>', methods=['POST'])
@login_required
def generate_receipt(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    payment_method = request.form.get('payment_method', 'Credit Card')
    
    # Create new receipt
    receipt = Receipt(booking=booking, payment_method=payment_method)
    db.session.add(receipt)
    db.session.commit()
    
    return redirect(url_for('booking.view_receipt', booking_id=booking_id))

# User routes for customer functionality
@user_bp.route('/dashboard')
@login_required
def dashboard():
    if not hasattr(current_user, 'is_customer') or not current_user.is_customer:
        flash('Access denied. This area is for customers only.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Fetch only pending or confirmed bookings for the current user
    bookings = Booking.query.filter_by(customer_id=current_user.id)\
                            .filter(Booking.status.in_(['pending', 'confirmed']))\
                            .order_by(Booking.booking_date.desc())\
                            .all()
    
    available_packages = TravelPackage.query.filter(TravelPackage.availability > 0).all()
    
    return render_template('user/dashboard.html', 
                         title='My Dashboard', 
                         bookings=bookings, 
                         available_packages=available_packages)

@user_bp.route('/packages')
@login_required
def view_packages():
    if not hasattr(current_user, 'is_customer') or not current_user.is_customer:
        flash('Access denied. This area is for customers only.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get all available packages
    packages = TravelPackage.query.filter(TravelPackage.availability > 0).all()
    
    return render_template('user/packages.html', title='Available Packages', packages=packages)

@user_bp.route('/packages/<int:id>')
@login_required
def view_package_details(id):
    if not hasattr(current_user, 'is_customer') or not current_user.is_customer:
        flash('Access denied. This area is for customers only.', 'danger')
        return redirect(url_for('auth.login'))
    
    package = TravelPackage.query.get_or_404(id)
    
    return render_template('user/package_details.html', title=package.name, package=package)

@user_bp.route('/book/<int:package_id>', methods=['GET', 'POST'])
@login_required
def book_package(package_id):
    if not hasattr(current_user, 'is_customer') or not current_user.is_customer:
        flash('Access denied. This area is for customers only.', 'danger')
        return redirect(url_for('auth.login'))
    
    package = TravelPackage.query.get_or_404(package_id)
    
    if request.method == 'POST':
        travel_date_str = request.form.get('travel_date')
        num_travelers = int(request.form.get('num_travelers'))
        
        # Validate form data
        if not travel_date_str:
            flash('Please select a travel date', 'danger')
            return redirect(url_for('user.book_package', package_id=package_id))
        
        if num_travelers <= 0 or num_travelers > package.availability:
            flash(f'Invalid number of travelers. Maximum available: {package.availability}', 'danger')
            return redirect(url_for('user.book_package', package_id=package_id))
        
        # Parse travel date
        travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d')
        
        # Calculate total price
        total_price = package.price * num_travelers
        
        # Create booking
        booking = Booking(
            customer_id=current_user.id,
            package_id=package_id,
            travel_date=travel_date,
            num_travelers=num_travelers,
            total_price=total_price,
            status='pending'
        )
        
        db.session.add(booking)
        
        # Update package availability
        package.availability -= num_travelers
        
        db.session.commit()
        
        flash('Booking created successfully!', 'success')
        return redirect(url_for('user.confirm_booking', booking_id=booking.id))
    
    return render_template('user/book_package.html', title=f"Book {package.name}", package=package)

@user_bp.route('/confirm/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def confirm_booking(booking_id):
    if not hasattr(current_user, 'is_customer') or not current_user.is_customer:
        flash('Access denied. This area is for customers only.', 'danger')
        return redirect(url_for('auth.login'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    # Ensure booking belongs to current user
    if booking.customer_id != current_user.id:
        flash('Access denied. This booking does not belong to you.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        
        # Update booking status
        booking.status = 'confirmed'
        
        # Calculate taxes and final amount
        tax_rate = 0.1  # 10% tax
        tax_amount = booking.total_price * tax_rate
        final_amount = booking.total_price + tax_amount
        
        # Generate receipt
        receipt = Receipt(
            booking=booking,
            payment_method=payment_method,
            payment_status='PAID'
        )
        
        db.session.add(receipt)
        db.session.commit()
        
        flash('Booking confirmed! Your receipt has been generated.', 'success')
        return redirect(url_for('user.view_receipt', receipt_id=receipt.id))
    
    return render_template('user/confirm_booking.html', title='Confirm Booking', booking=booking)

@user_bp.route('/receipt/<int:receipt_id>')
@login_required
def view_receipt(receipt_id):
    if not hasattr(current_user, 'is_customer') or not current_user.is_customer:
        flash('Access denied. This area is for customers only.', 'danger')
        return redirect(url_for('auth.login'))
    
    receipt = Receipt.query.get_or_404(receipt_id)
    booking = receipt.booking
    
    # Ensure receipt belongs to current user
    if booking.customer_id != current_user.id:
        flash('Access denied. This receipt does not belong to you.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    return render_template('user/receipt.html', title='Receipt', receipt=receipt, booking=booking)
