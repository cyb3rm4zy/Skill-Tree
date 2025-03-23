from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
import re

bp = Blueprint('auth', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    return 3 <= len(username) <= 20 and username.isalnum()

def validate_password(password):
    return len(password) >= 8

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            
            # Validate input
            if not username or not email or not password:
                flash('All fields are required', 'error')
                return redirect(url_for('auth.register'))
                
            if not validate_username(username):
                flash('Username must be 3-20 characters long and contain only letters and numbers', 'error')
                return redirect(url_for('auth.register'))
                
            if not validate_email(email):
                flash('Please enter a valid email address', 'error')
                return redirect(url_for('auth.register'))
                
            if not validate_password(password):
                flash('Password must be at least 8 characters long', 'error')
                return redirect(url_for('auth.register'))
            
            # Check if username or email already exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'error')
                return redirect(url_for('auth.register'))
                
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return redirect(url_for('auth.register'))
            
            # Create user
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
            
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error: {str(e)}")
            flash('An error occurred during registration', 'error')
            return redirect(url_for('auth.register'))
        
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            
            if not username or not password:
                flash('Please enter both username and password', 'error')
                return redirect(url_for('auth.login'))
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Invalid username or password', 'error')
                return redirect(url_for('auth.login'))
                
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            flash('An error occurred during login', 'error')
            return redirect(url_for('auth.login'))
        
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.index')) 