from flask import Blueprint, jsonify, request, current_app
from .services.discord_notifier import send_notification
import os

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/social/status', methods=['GET'])
def get_social_status():
    pihole = current_app.config['PIHOLE_CLIENT']
    status = pihole.get_status()
    return jsonify({"status": status})

@api_v1.route('/social/toggle', methods=['POST'])
def toggle_social_status():
    pihole = current_app.config['PIHOLE_CLIENT']
    socketio = current_app.config['SOCKETIO']
    client_ip = current_app.config['CLIENT_IP']
    
    target_action = request.json.get('action') # 'block' or 'unblock'
    enabled = (target_action == 'block')
    
    new_status = pihole.set_social_block(client_ip, enabled=enabled)
    
    if new_status != "Error":
        send_notification(new_status)
        socketio.emit('status_change', {'status': new_status}, namespace='/')
        return jsonify({"success": True, "status": new_status})
    else:
        return jsonify({"success": False, "message": "Failed to toggle status"}), 500
