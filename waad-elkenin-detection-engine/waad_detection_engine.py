import requests
import redis
import json
import hashlib
import re
from datetime import datetime

API_URL = "http://3.145.146.136:5000/api/add-detection"

def send_alert(event_type, source_ip, description, severity="medium"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "event_type": event_type,
        "source_ip": source_ip,
        "ip_address": source_ip,    # CRITICAL: Victoria expects this!
        "description": f"{timestamp} - {description}",
        "severity": severity
    }

    print(f"[API] Sending alert: {event_type} from {source_ip}")

    try:
        response = requests.post(API_URL, json=data, timeout=5)
        print(f"[API] Status: {response.status_code}")

        if response.status_code == 200:
            print(f"[API] Success: {response.text}")
        else:
            print(f"[API] Error {response.status_code}: {response.text}")
            with open('api_failures.log', 'a') as f:
                f.write(f"{datetime.now().isoformat()}: STATUS={response.status_code}, DATA={json.dumps(data)}\n")
    except Exception as e:
        print(f"[API] Exception: {e}")
        with open('api_failures.log', 'a') as f:
            f.write(f"{datetime.now().isoformat()}: EXCEPTION={str(e)}, DATA={json.dumps(data)}\n")

class DetectionEngine:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=False)
        self.redis.ping()

    def process_event(self, event):
        alerts = []

        alert = self.detect_brute_force(event)
        if alert:
            alerts.append(alert)
            send_alert("ssh_bruteforce", alert['source_ip'], alert['description'], alert['severity'])

        alert = self.detect_powershell_abuse(event)
        if alert:
            alerts.append(alert)
            send_alert("powershell_abuse", alert['source_ip'], alert['description'], alert['severity'])

        alert = self.detect_ssh_anomaly(event)
        if alert:
            alerts.append(alert)
            send_alert("suspicious_login", alert['source_ip'], alert['description'], alert['severity'])

        alert = self.detect_privilege_escalation(event)
        if alert:
            alerts.append(alert)
            send_alert("privilege_escalation", alert['source_ip'], alert['description'], alert['severity'])

        return alerts

    def detect_brute_force(self, event):
        if event.get('event_type') not in ['failed_login', 'authentication_failure']:
            return None

        source_ip = event.get('source_ip', 'unknown')
        username = event.get('username')

        key = f"brute:{source_ip}:{username or 'unknown'}"
        now = datetime.now().timestamp()

        pipe = self.redis.pipeline()
        pipe.zadd(key, {json.dumps(event): now})
        pipe.zremrangebyscore(key, 0, now - 120)
        pipe.zcard(key)
        pipe.expire(key, 180)
        results = pipe.execute()

        count = results[2]

        if count >= 5:
            minute_key = f"minute_brute:{source_ip}"
            minute_count = self.redis.incr(minute_key)
            if minute_count == 1:
                self.redis.expire(minute_key, 60)

            if minute_count >= 10:
                send_alert("ssh_bruteforce", source_ip, f"{minute_count} failed logins in 1 minute", "critical")

            alert_id = f"brute_{int(now)}_{hashlib.md5(source_ip.encode()).hexdigest()[:8]}"

            return {
                'alert_id': alert_id,
                'timestamp': datetime.now().isoformat(),
                'severity': 'critical',
                'title': f"Brute Force Attack from {source_ip}",
                'description': f"{count} failed logins in 2 minutes",
                'source_ip': source_ip,
                'username': username,
                'attack_type': 'brute_force'
            }
        return None

    def detect_powershell_abuse(self, event):
        process = event.get('process_name', '').lower()
        if process not in ['powershell.exe', 'pwsh.exe', 'powershell', 'pwsh']:
            return None

        command_line = event.get('command_line', '').lower()
        source_ip = event.get('source_ip', 'localhost')
        username = event.get('username')

        patterns = [
            r'-encodedcommand\s+[a-z0-9+/=]{20,}',
            r'-windowstyle\s+hidden',
            r'iex\s*\(.*new-object\s+net\.webclient',
            r'invoke-expression\s+.*downloadstring',
            r'powershell.*-exec\s+bypass.*-command',
            r'start-process.*-windowstyle\s+hidden',
            r'-nop\s+-w\s+hidden\s+-enc',
            r'frombasestring.*system\.text\.encoding'
        ]

        matched = []
        for pattern in patterns:
            if re.search(pattern, command_line, re.IGNORECASE):
                matched.append(pattern)

        if matched:
            alert_id = f"ps_{int(datetime.now().timestamp())}_{hashlib.md5(command_line[:50].encode()).hexdigest()[:8]}"

            return {
                'alert_id': alert_id,
                'timestamp': datetime.now().isoformat(),
                'severity': 'high',
                'title': "Suspicious PowerShell Activity",
                'description': f"PowerShell matched {len(matched)} suspicious patterns",
                'source_ip': source_ip,
                'username': username,
                'attack_type': 'powershell_abuse'
            }
        return None

    def detect_ssh_anomaly(self, event):
        if event.get('service') != 'ssh' and event.get('process_name') != 'sshd':
            return None

        source_ip = event.get('source_ip')
        username = event.get('username')

        anomalies = []

        if username == 'root' and event.get('event_type') == 'failed_login':
            key = f"ssh_root:{source_ip}"
            attempts = self.redis.incr(key)
            self.redis.expire(key, 3600)

            if attempts >= 3:
                anomalies.append(f"root_attempts({attempts})")

        hour = datetime.now().hour
        if hour in [0, 1, 2, 3, 4, 5, 22, 23]:
            anomalies.append(f"off_hours({hour}:00)")

        if anomalies:
            alert_id = f"ssh_{int(datetime.now().timestamp())}_{hashlib.md5(source_ip.encode()).hexdigest()[:8]}"

            return {
                'alert_id': alert_id,
                'timestamp': datetime.now().isoformat(),
                'severity': 'high',
                'title': "SSH Anomaly Detected",
                'description': f"SSH anomalies: {', '.join(anomalies)}",
                'source_ip': source_ip,
                'username': username,
                'attack_type': 'ssh_anomaly'
            }
        return None

    def detect_privilege_escalation(self, event):
        command_line = event.get('command_line', '').lower()
        source_ip = event.get('source_ip', 'localhost')
        username = event.get('username')

        patterns = [
            r'sudo\s+su(\s+|$)',
            r'sudo\s+passwd',
            r'usermod.*-ag\s+(sudo|admin|wheel)',
            r'chmod\s+[0-9]+\s+/etc/sudoers',
            r'echo.*sudoers',
            r'setuid|setgid.*/bin',
            r'chown.*root:root.*/bin'
        ]

        matched = []
        for pattern in patterns:
            if re.search(pattern, command_line, re.IGNORECASE):
                matched.append(pattern)

        if matched:
            sequence_key = f"cmd_seq:{username or 'unknown'}"
            self.redis.lpush(sequence_key, command_line[:100])
            self.redis.ltrim(sequence_key, 0, 9)
            self.redis.expire(sequence_key, 300)

            alert_id = f"priv_{int(datetime.now().timestamp())}_{hashlib.md5(source_ip.encode()).hexdigest()[:8]}"

            return {
                'alert_id': alert_id,
                'timestamp': datetime.now().isoformat(),
                'severity': 'critical',
                'title': "Privilege Escalation Attempt",
                'description': "Suspicious privilege escalation patterns detected",
                'source_ip': source_ip,
                'username': username,
                'attack_type': 'privilege_escalation'
            }
        return None
