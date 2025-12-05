import requests
import json

url = "http://localhost:5000"

print("Testing alert system...")

# Test 1: Send HIGH alert
alert_data = {
    "event_type": "unauthorized",
    "source_ip": "10.0.0.99",
    "description": "Failed login attempts",
    "severity": "HIGH"
}

try:
    response = requests.post(f"{url}/api/add-detection", json=alert_data)
    print(f"High alert: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Send MEDIUM alert
alert_data = {
    "event_type": "scan",
    "source_ip": "192.168.1.50",
    "description": "Port scan detected",
    "severity": "MEDIUM"
}

try:
    response = requests.post(f"{url}/api/add-detection", json=alert_data)
    print(f"Medium alert: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Get all alerts
try:
    response = requests.get(f"{url}/api/security-alerts")
    data = response.json()
    print(f"Total alerts: {data['total']}")
except Exception as e:
    print(f"Error: {e}")
