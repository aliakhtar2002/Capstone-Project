#!/usr/bin/env python3
import requests

API = "http://localhost:5000/api"

print("=== AAL4 Test Audit ===")
print()

# Test 1: Health
try:
    r = requests.get(f"{API}/health")
    if r.status_code == 200:
        data = r.json()
        print(f"[PASS] API Health: {data['status']}, detections: {data['detections_count']}")
    else:
        print(f"[FAIL] API Health: {r.status_code}")
except:
    print("[FAIL] API Health: Connection failed")

# Test 2: Add detection
try:
    payload = {"event_type": "test", "ip_address": "192.168.1.99", "severity": "medium"}
    r = requests.post(f"{API}/add-detection", json=payload)
    if r.status_code == 200:
        print(f"[PASS] Add detection: ID {r.json()['detection_id']}")
    else:
        print(f"[FAIL] Add detection: {r.status_code}")
except:
    print("[FAIL] Add detection: Failed")

# Test 3: Get events
try:
    r = requests.get(f"{API}/security-events")
    if r.status_code == 200:
        data = r.json()
        print(f"[PASS] Get events: {data['count']} detections")
    else:
        print(f"[FAIL] Get events: {r.status_code}")
except:
    print("[FAIL] Get events: Failed")

print()
print("=== Test Audit Complete ===")
