
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

PIHOLE_URL = os.getenv('PIHOLE_URL')
PIHOLE_PASSWORD = os.getenv('PIHOLE_PASSWORD')

def test_connection():
    print(f"Testing connection to: {PIHOLE_URL}")
    print("-" * 50)

    # 1. Test Base URL Reachability
    try:
        print("1. Checking simple connectivity...")
        response = requests.get(f"{PIHOLE_URL}/admin/", timeout=5)
        print(f"   [PASS] Reachable (Status: {response.status_code})")
    except Exception as e:
        print(f"   [FAIL] Could not reach PiHole: {e}")
        return

    # 2. Test Authentication
    print("\n2. Testing Authentication...")
    url = f"{PIHOLE_URL}/api/auth/"
    payload = {"password": PIHOLE_PASSWORD}
    session = requests.Session()
    
    try:
        response = session.post(url, json=payload)
        data = response.json()
        
        if data.get("session", {}).get("valid"):
            print("   [PASS] Login Successful")
            sid = data["session"]["sid"]
            print(f"   SID: {sid[:10]}...")
            session.headers.update({"X-FTL-SID": sid})
        else:
            print(f"   [FAIL] Login Failed: {data}")
            return
    except Exception as e:
        print(f"   [FAIL] Auth Request Error: {e}")
        return

    # 3. Test Group Fetching (Read Access)
    print("\n3. Testing Group Access (Reading 'Social')...")
    try:
        # Try to read the group to see if we have permissions/access
        # Note: This URL might need adjustment based on specific API version
        url = f"{PIHOLE_URL}/api/groups/Social"
        response = session.get(url)
        
        if response.status_code == 200:
            print(f"   [PASS] Group 'Social' found: {response.text}")
        elif response.status_code == 404:
             print("   [WARN] Group 'Social' NOT found. Please create it in PiHole.")
        else:
            print(f"   [FAIL] Error accessing group: {response.status_code}")
    except Exception as e:
        print(f"   [FAIL] Group Request Error: {e}")

    print("-" * 50)
    print("Done.")

if __name__ == "__main__":
    test_connection()
