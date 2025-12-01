import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    try:
        print("Testing /api/health...")
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_detection_post():
    try:
        print("Testing POST /api/detections...")
        test_data = {
            "event_type": "brute_force", 
            "ip_address": "192.168.1.100",
            "severity": "high"
        }
        response = requests.post(f"{BASE_URL}/api/detections", json=test_data)
        if response.status_code == 200:
            print("✅ Detection POST working")
            return True
        else:
            print(f"❌ Detection POST failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Detection POST error: {e}")
        return False

def test_security_events():
    try:
        print("Testing /api/security-events...")
        response = requests.get(f"{BASE_URL}/api/security-events")
        if response.status_code == 200:
            print("✅ Security events endpoint working")
            return True
        else:
            print(f"❌ Security events failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Security events error: {e}")
        return False

def test_dashboard_stats():
    try:
        print("Testing /api/dashboard/stats...")
        response = requests.get(f"{BASE_URL}/api/dashboard/stats")
        if response.status_code == 200:
            print("✅ Dashboard stats working")
            return True
        else:
            print(f"❌ Dashboard stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard stats error: {e}")
        return False

if __name__ == "__main__":
    print("Running API Tests...")
    
    tests = [
        test_health_endpoint,
        test_detection_post, 
        test_security_events,
        test_dashboard_stats
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed")
