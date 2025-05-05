import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from app import db
from models import User
from forms import LoginForm, RegistrationForm
from utils.key_management import generate_salt

# Create blueprint
auth = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    # Redirect if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('diary.dashboard'))
    
    # Create login form
    form = LoginForm()
    
    # Handle form submission
    if form.validate_on_submit():
        try:
            # Find user by username (will be decrypted in query)
            users = User.query.all()
            user = None
            for u in users:
                if u.username == form.username.data:
                    user = u
                    break
            
            # Check user and password
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password', 'danger')
                logger.warning(f"Failed login attempt for username: {form.username.data}")
                return redirect(url_for('auth.login'))
            
            # Log user in
            login_user(user, remember=form.remember_me.data)
            logger.info(f"User logged in: {user.id}")
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('diary.dashboard')
            
            flash('Login successful!', 'success')
            return redirect(next_page)
        
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            flash('An error occurred during login. Please try again.', 'danger')
    
    # Render login template
    return render_template('login.html', title='Sign In', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    # Redirect if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('diary.dashboard'))
    
    # Create registration form
    form = RegistrationForm()
    
    # Handle form submission
    if form.validate_on_submit():
        try:
            # Generate a unique salt for this user
            salt = generate_salt()
            
            # Create new user
            user = User(salt=salt)
            user.username = form.username.data
            user.email = form.email.data
            user.set_password(form.password.data)
            
            # Save user to database
            db.session.add(user)
            db.session.commit()
            logger.info(f"New user registered: {user.id}")
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
    
    # Render registration template
    return render_template('register.html', title='Register', form=form)

@auth.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
