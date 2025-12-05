#!/usr/bin/env python3
# Test script for SOC Alerting System

import requests
import json
import time

API_URL = "http://localhost:5000"

def test_alert_system():
    print("Testing SOC Alert System...")
    print("="*50)
    
    # Test 1: Check health endpoint
    print("\n1. Testing health endpoint:")
    try:
        resp = requests.get(f"{API_URL}/api/health")
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {resp.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Send a test alert
    print("\n2. Sending test alert:")
    test_alert = {
        "event_type": "unauthorized_access",
        "source_ip": "10.0.1.50",
        "description": "Multiple failed login attempts",
        "severity": "HIGH"
    }
    
    try:
        resp = requests.post(f"{API_URL}/api/add-detection", json=test_alert)
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {resp.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Get all alerts
    print("\n3. Getting all alerts:")
    try:
        resp = requests.get(f"{API_URL}/api/security-alerts")
        data = resp.json()
        print(f"   Status: {resp.status_code}")
        print(f"   Total alerts: {data['total']}")
        print(f"   Last alert: {data['alerts'][-1] if data['alerts'] else 'None'}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Send different severity alerts
    print("\n4. Testing different severity levels:")
    severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    
    for severity in severities:
        alert = {
            "event_type": f"test_{severity.lower()}",
            "source_ip": f"192.168.1.{ord(severity[0]) % 256}",
            "description": f"Test {severity} severity alert",
            "severity": severity
        }
        
        try:
            resp = requests.post(f"{API_URL}/api/add-detection", json=alert)
            if resp.status_code == 200:
                print(f"   {severity}: PASS - Sent successfully")
            else:
                print(f"   {severity}: FAIL - API error")
        except:
            print(f"   {severity}: FAIL - Connection error")
    
    print("\n" + "="*50)
    print("Alert system test complete.")
    print("Check the console output from app.py for alert processing.")

if __name__ == "__main__":
    test_alert_system()
