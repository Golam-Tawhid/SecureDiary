import os
import logging
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Create SQLAlchemy instance
db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object('config.Config')

# Security setup
app.secret_key = app.config['SECRET_KEY']
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
# Removed direct override of SQLALCHEMY_DATABASE_URI to use config.py value instead
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Create database tables
with app.app_context():
    # Import models after initializing db to avoid circular imports
    from models import User, DiaryEntry
    db.create_all()
    logger.info("Database tables created")

# Register blueprints
from routes.auth import auth
from routes.diary import diary

app.register_blueprint(auth)
app.register_blueprint(diary)

# Add context processor for templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
