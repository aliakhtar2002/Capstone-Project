#!/usr/bin/env python3
import subprocess
import requests

def check_api_security():
    print(" Scanning API Security...")
    
    # Test if debug mode is enabled
    response = requests.get('http://localhost:5000/api/health')
    if 'debug' in response.text.lower():
        print(" DEBUG MODE ENABLED - Security Risk")
    
    # Test endpoint without auth
    test_data = {"event_type": "test", "ip_address": "127.0.0.1", "severity": "high"}
    response = requests.post('http://localhost:5000/api/detections', json=test_data)
    if response.status_code == 200:
        print(" NO AUTHENTICATION - Anyone can send data")
    
    print(" Security scan completed")

if __name__ == "__main__":
    check_api_security()
