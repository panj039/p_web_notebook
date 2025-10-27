import json
import bcrypt
import pyotp
import sys
from pathlib import Path
from functools import wraps
from flask import request, session, redirect, url_for, render_template, flash

# Add util to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent))
from util.paths import get_users_config_file

USERS_CONFIG_FILE = get_users_config_file()


def load_users() -> dict[str, dict]:
    """Load users from config/users.json file"""
    try:
        with open(USERS_CONFIG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {u['username']: u for u in data['users']}
    except FileNotFoundError:
        return {}


def check_password(username: str, password: str) -> bool:
    """Check if password is correct for given username"""
    users = load_users()
    if username not in users:
        return False
    
    stored_hash = users[username]['password_hash']
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))


def check_totp(username: str, token: str) -> bool:
    """Check if TOTP token is valid for given username"""
    users = load_users()
    if username not in users:
        return False
    
    totp_secret = users[username]['totp_secret']
    totp = pyotp.TOTP(totp_secret)
    return totp.verify(token)


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def handle_login():
    """Handle login form submission"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        otp = request.form.get('otp', '').strip()
        
        if not username or not password or not otp:
            flash('All fields are required', 'error')
            return render_template('login.html')
        
        if check_password(username, password) and check_totp(username, otp):
            session['user'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials or verification code', 'error')
            return render_template('login.html')
    
    return render_template('login.html')


def handle_logout():
    """Handle logout"""
    session.pop('user', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))