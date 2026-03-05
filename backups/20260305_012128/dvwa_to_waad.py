#!/usr/bin/env python3
import time
import re
import requests
from datetime import datetime

API_URL = "http://3.145.146.136:5000/api/add-detection"
LOG_FILE = "/var/log/httpd/access_log"

def send_alert(event_type, ip, description, severity="medium"):
    data = {
        "event_type": event_type,
        "ip_address": ip,
        "description": description,
        "severity": severity
    }
    try:
        requests.post(API_URL, json=data, timeout=2)
    except:
        pass

def follow_log():
    with open(LOG_FILE, 'r') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            # Parse Apache log
            match = re.search(r'(\d+\.\d+\.\d+\.\d+).*"(GET|POST).*?((?:sqli|brute|xss|fi).*?) HTTP', line.lower())
            if match:
                ip = match.group(1)
                url = match.group(3)
                
                if 'sqli' in url or 'id=' in line and '%27' in line:
                    send_alert('sql_injection', ip, 'SQLi attempt detected', 'critical')
                elif 'brute' in url or 'login' in line and 'POST' in line:
                    send_alert('brute_force', ip, 'Brute force attempt', 'high')
                elif 'xss' in url or '<script' in line:
                    send_alert('xss', ip, 'XSS attempt', 'high')
                elif 'fi' in url or 'page=' in line and '../' in line:
                    send_alert('idor', ip, 'IDOR attempt', 'high')

if __name__ == "__main__":
    follow_log()
