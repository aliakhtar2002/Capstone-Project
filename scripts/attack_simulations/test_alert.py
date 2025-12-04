import requests

# Send a test alert to Aishat's dashboard
response = requests.post(
    "http://3.145.146.136:5000/api/add-detection",
    json={
        "event_type": "test_alert",
        "source_ip": "10.0.0.99",
        "description": "Test alert from Victoria",
        "severity": "info",
        "simulated_by": "victoria"
    }
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
