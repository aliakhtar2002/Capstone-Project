#!/usr/bin/env python3
import requests
import time
import random
from datetime import datetime

API_URL = "http://3.145.146.136:5000/api/add-detection"

def send_alert(event_type, ip, desc, severity="medium"):
    data = {
        "event_type": event_type,
        "source_ip": ip,
        "description": desc,
        "severity": severity,
        "timestamp": datetime.now().isoformat(),
        "simulated_by": "victoria"
    }
    try:
        print(f"[Victoria] Sending: {event_type}")
        r = requests.post(API_URL, json=data, timeout=5)
        print(f"  Status: {r.status_code}")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

print("="*60)
print("VICTORIA: Sending attack simulations to API")
print("="*60)

# VOSF1: Hydra simulation
send_alert("ssh_bruteforce", f"10.0.0.{random.randint(100,200)}", 
           "Hydra SSH brute force: 15 failed attempts", "critical")
time.sleep(1)

# VOSF1: Nmap simulation  
send_alert("port_scan", f"192.168.99.{random.randint(1,100)}", 
           "Nmap stealth scan: 50 ports scanned", "high")
time.sleep(1)

# VOSF2: PowerShell simulation
send_alert("powershell_abuse", f"172.16.0.{random.randint(50,150)}", 
           "PowerShell attack: malware download attempt", "critical")
time.sleep(1)

# VOSF3: Sudo abuse simulation
send_alert("sudo_privilege_escalation", f"10.10.10.{random.randint(1,50)}", 
           "Sudo abuse: 4 privilege escalation attempts", "high")
time.sleep(1)

# VOSF4: Rapid logins simulation
send_alert("rapid_failed_logins", f"203.0.113.{random.randint(1,255)}", 
           "Rapid failed logins: 22 attempts in 1 minute", "critical")

print("\n" + "="*60)
print("Done! 5 attack simulations sent to API")
print("Check dashboard: http://3.145.146.136:8080")
print("="*60)
