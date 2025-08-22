# AI GENERATED

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 10

def test_server_alive():
    """Test if the server is running"""
    print("🔍 Testing if server is alive...")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=TIMEOUT)
        print(f"✅ Server is alive! Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server! Check if it's running.")
        return False
    except requests.exceptions.Timeout:
        print("❌ Server connection timed out!")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_payload(payload: dict, expected_sc: int, send_saved: int = 0, output: bool = True):
    try:
        response = requests.post(
            f"{BASE_URL}/notify?send_saved={send_saved}", 
            json=payload, 
            timeout=TIMEOUT,
            headers={"Content-Type": "application/json"}
        )
        if output:
            if response.status_code == expected_sc:
                print(f"Status Code: {response.status_code}")
                print("✅ Server reacted correctly")
            else:
                print(f"⚠️ Expected {expected_sc} but got: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_delete():
    try:
        response = requests.delete(f"{BASE_URL}/clear", timeout=TIMEOUT)
        if response.status_code == 200:
            print(f"Status Code: {response.status_code}")
            print(response.text)
            print("✅ Server reacted correctly")
        else:
            print(f"⚠️ Got status code {response.status_code} wtf even happened??")  
    except Exception as e:
        print(f"❌ Error: {e}")

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting API Tests...\n")
    print("=" * 50)
    
    # Test 1: Server alive
    if not test_server_alive():
        print("\n❌ Server is not responding. Cannot continue with tests.")
        return
    
    print("\n📨 Testing warning payload...")
    payload = {"type": "warning", "name": "warning payload", "description": "very descriptive description"}
    test_payload(payload, 200)

    print("\n📨 Testing info payload...")
    payload = {"type": "info", "name": "info payload", "description": "very descriptive description"}
    test_payload(payload, 200)

    print("\n📨 Testing warning payload with query param...")
    payload = {"type": "warning", "name": "warning payload", "description": "very descriptive description"}
    test_payload(payload, 200, 10)

    print("\n📨 Testing invalid payload...")
    payload = {"type": "invalid", "name": "invalid payload"}
    test_payload(payload, 422)
    
    print("\n📨 Testing delete...")
    test_delete()

    print("\n📨 Adding messages to delete...")
    payload = {"type": "info", "name": "info payload", "description": "very descriptive description"}
    for _ in range(5):
        test_payload(payload, 200, output=False)

    print("\n📨 Testing delete...")
    test_delete()

    print("\n" + "=" * 50)
    print("🏁 Tests completed!")

if __name__ == "__main__":
    run_all_tests()