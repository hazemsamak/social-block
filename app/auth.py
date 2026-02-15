from flask import session, redirect, url_for, request, jsonify
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            if request.path.startswith('/api/v1'):
                return jsonify({"error": "Unauthorized", "message": "Session expired"}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
