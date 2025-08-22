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

def test_warning_notification():
    """Test sending a Warning notification (should be forwarded)"""
    print("\n📨 Testing Warning notification...")
    
    payload = {
        "type": "Warning",
        "name": "Test Warning Alert",
        "description": "This is a test warning notification from the test script"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/notify", 
            json=payload, 
            timeout=TIMEOUT,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Warning notification sent successfully!")
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out! Check your webhook or server code.")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Server might not be running.")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_info_notification():
    """Test sending an Info notification (should NOT be forwarded)"""
    print("\n📨 Testing Info notification...")
    
    payload = {
        "type": "Info",
        "name": "Test Info Message",
        "description": "This is a test info notification that should be filtered out"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/notify", 
            json=payload, 
            timeout=TIMEOUT,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Info notification processed successfully!")
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out!")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed!")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_invalid_payload():
    """Test sending invalid data"""
    print("\n📨 Testing invalid payload...")
    
    payload = {
        "invalid": "data",
        "missing": "required_fields"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/notify", 
            json=payload, 
            timeout=TIMEOUT,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("✅ Server correctly rejected invalid payload!")
        else:
            print(f"⚠️ Expected 422 but got: {response.status_code}")
            
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
    
    # Test 2: Warning notification
    test_warning_notification()
    
    # Test 3: Info notification  
    test_info_notification()
    
    # Test 4: Invalid payload
    test_invalid_payload()
    
    print("\n" + "=" * 50)
    print("🏁 Tests completed!")

if __name__ == "__main__":
    run_all_tests()