
from datetime import timedelta
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import os
from dotenv import load_dotenv
from .services.pihole_client import PiHoleClient
from .services.discord_notifier import send_notification
from functools import wraps
from flask_socketio import SocketIO, emit

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Set secret key for sessions
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key') 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31) 

socketio = SocketIO(app, cors_allowed_origins="*")

pihole = PiHoleClient()

CLIENT_IP = os.getenv('CLIENT_IP', '192.168.1.0/24')
APP_PASSWORD = os.getenv('APP_PASSWORD', 'admin')

# Attach dependencies to app config for Blueprint access
app.config['PIHOLE_CLIENT'] = pihole
app.config['SOCKETIO'] = socketio
app.config['CLIENT_IP'] = CLIENT_IP

# Register Blueprints
from .api import api_v1
app.register_blueprint(api_v1, url_prefix='/api/v1')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == APP_PASSWORD:
            session.permanent = True
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid Password'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # Logout from PiHole
    pihole.logout()
    
    # Clear local session
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')
