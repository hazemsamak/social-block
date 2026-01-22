
import requests
import os
import json

def send_notification(status):
    """Sends a notification to Discord via Webhook."""
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url or webhook_url == "your_discord_webhook_url_here":
        print("Discord Webhook URL not configured.")
        return False

    message = f":shield: **PiHole Status Update** :shield:\n\nSocial Media is now **{status}**."
    
    data = {
        "content": message
    }
    
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code in [200, 204]:
            return True
        else:
            print(f"Failed to send Discord notification: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error sending Discord notification: {e}")
        return False
