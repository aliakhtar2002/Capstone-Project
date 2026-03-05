import time
import requests
import re

def extract_ip(line):
    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
    return match.group(1) if match else '0.0.0.0'

def detect_attack_type(line):
    if 'sql' in line.lower() or '%27' in line or 'SELECT' in line:
        return 'sqli_test', 'critical'
    elif '<script>' in line or 'alert(' in line:
        return 'xss_test', 'high'
    else:
        return 'suspicious_activity', 'medium'

def follow_log():
    with open('/var/log/httpd/access_log', 'r') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if line:
                print(f"Found: {line.strip()}")
                try:
                    event_type, severity = detect_attack_type(line)
                    ip_address = extract_ip(line)
                    
                    requests.post(
                        'http://localhost:5000/api/add-detection',
                        json={
                            'event_type': event_type,
                            'ip_address': ip_address,
                            'severity': severity
                        },
                        timeout=1
                    )
                except:
                    pass
            time.sleep(0.1)

if __name__ == "__main__":
    follow_log()
