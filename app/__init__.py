from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from datetime import datetime

# Initialize SQLAlchemy extension
db = SQLAlchemy()
# Initialize Login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from app.routes import main_bp, auth_bp, package_bp, customer_bp, booking_bp, user_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(package_bp, url_prefix='/packages')
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(booking_bp, url_prefix='/bookings')
    app.register_blueprint(user_bp, url_prefix='/user')
    
    # Add context processor for templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    return app
