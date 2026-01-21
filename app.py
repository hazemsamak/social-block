
from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv
from pihole_client import PiHoleClient
from discord_notifier import send_notification

# Load environment variables
load_dotenv()

app = Flask(__name__)
pihole = PiHoleClient()

CLIENT_IP = os.getenv('CLIENT_IP', '192.168.1.0/24')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    status = pihole.get_status()
    return jsonify({"status": status})

@app.route('/api/toggle', methods=['POST'])
def toggle_status():
    current_status = pihole.get_status()
    
    # Logic: 
    # If blocked, we want to unblock (Disable Group, Remove Client)
    # If unblocked, we want to block (Enable Group, Add Client)
    
    # However, user request says:
    # "For Unblock: Delete client and disable Group"
    # "For Block: Enable Group and add client"
    
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
