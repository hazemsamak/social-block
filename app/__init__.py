
from datetime import timedelta
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import os
from dotenv import load_dotenv
from .services.pihole_client import PiHoleClient
from .services.discord_notifier import send_notification
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Set secret key for sessions
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key') 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31) 

pihole = PiHoleClient()

CLIENT_IP = os.getenv('CLIENT_IP', '192.168.1.0/24')
APP_PASSWORD = os.getenv('APP_PASSWORD', 'admin')

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

@app.route('/api/status', methods=['GET'])
@login_required
def get_status():
    status = pihole.get_status()
    return jsonify({"status": status})

@app.route('/api/toggle', methods=['POST'])
@login_required
def toggle_status():
    current_status = pihole.get_status()
    
    target_action = request.json.get('action') # 'block' or 'unblock'
    
    success = False
    new_status = "Unknown"
    
    if target_action == 'block':
        # Enable Group
        if pihole.toggle_group("Social", enable=True):
            # Add Client
            pihole.add_client_to_group(CLIENT_IP, "Social")
            success = True
            new_status = "Blocked"
    elif target_action == 'unblock':
        # Disable Group
        if pihole.toggle_group("Social", enable=False):
            # Remove Client
            pihole.remove_client(CLIENT_IP)
            success = True
            new_status = "Unblocked"
            
    if success:
        send_notification(new_status)
        return jsonify({"success": True, "status": new_status})
    else:
        return jsonify({"success": False, "message": "Failed to toggle status"}), 500
