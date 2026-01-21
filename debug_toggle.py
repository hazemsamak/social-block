
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

PIHOLE_URL = os.getenv('PIHOLE_URL')
PIHOLE_PASSWORD = os.getenv('PIHOLE_PASSWORD')

def debug_toggle():
    print(f"Debugging Toggle on: {PIHOLE_URL}")
    
    # 1. Login
    session = requests.Session()
    auth_url = f"{PIHOLE_URL}/api/auth/"
    try:
        resp = session.post(auth_url, json={"password": PIHOLE_PASSWORD})
        data = resp.json()
        if data.get("session", {}).get("valid"):
            sid = data["session"]["sid"]
            session.headers.update({"X-FTL-SID": sid})
            print(f"[PASS] Logged in. SID: {sid[:5]}...")
        else:
            print(f"[FAIL] Login failed: {data}")
            return
    except Exception as e:
        print(f"[FAIL] Auth Error: {e}")
        return

    # 2. Check Current Status
    group_url = f"{PIHOLE_URL}/api/groups/Social"
    print(f"\nChecking current status of 'Social'...")
    try:
        r = session.get(group_url)
        print(f"GET Status: {r.status_code}")
        print(f"GET Body: {r.text}")
    except Exception as e:
        print(f"GET Error: {e}")

    # 3. Try to Enable (Block)
    print(f"\nAttempting to ENABLE 'Social' (BLOCK)...")
    payload = {"enabled": True}
    try:
        r = session.put(group_url, json=payload)
        print(f"PUT Status: {r.status_code}")
        print(f"PUT Body: {r.text}")
    except Exception as e:
        print(f"PUT Error: {e}")

    # 4. Check Status Again
    print(f"\nChecking status after update...")
    try:
        r = session.get(group_url)
        print(f"GET Body: {r.text}")
    except Exception as e:
        print(f"GET Error: {e}")

if __name__ == "__main__":
    debug_toggle()
