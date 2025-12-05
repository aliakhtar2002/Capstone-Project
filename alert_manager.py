# Alert Manager for SOC System
# Handles sending alerts to different channels

import json
import time
from datetime import datetime

class AlertManager:
    def __init__(self):
        self.alerts_history = []
        self.alert_count = 0
    
    def create_alert(self, title, description, severity, source_ip=None):
        """Create a new alert"""
        self.alert_count += 1
        
        alert = {
            "id": self.alert_count,
            "title": title,
            "description": description,
            "severity": severity.upper(),
            "source_ip": source_ip,
            "timestamp": datetime.now().isoformat(),
            "status": "NEW"
        }
        
        self.alerts_history.append(alert)
        
        # Send to appropriate channels based on severity
        self._route_alert(alert)
        
        return alert
    
    def _route_alert(self, alert):
        """Route alert based on severity"""
        severity = alert["severity"]
        
        print(f"=== ALERT [{severity}] ===")
        print(f"Title: {alert['title']}")
        print(f"Description: {alert['description']}")
        print(f"Time: {alert['timestamp']}")
        
        if severity in ["CRITICAL", "HIGH"]:
            self._send_immediate_alert(alert)
            self._log_to_file(alert)
        elif severity == "MEDIUM":
            self._send_security_alert(alert)
            self._log_to_file(alert)
        else:  # LOW or INFO
            self._log_only(alert)
    
    def _send_immediate_alert(self, alert):
        """Send immediate alert (for HIGH/CRITICAL)"""
        print("ACTION: Immediate alert sent")
        # Here we would add Slack/Email integration
    
    def _send_security_alert(self, alert):
        """Send security alert (for MEDIUM)"""
        print("ACTION: Security alert sent")
    
    def _log_only(self, alert):
        """Just log the alert (for LOW)"""
        print("ACTION: Logged only")
    
    def _log_to_file(self, alert):
        """Log alert to file"""
        try:
            with open("security_alerts.log", "a") as f:
                f.write(json.dumps(alert) + "\n")
        except:
            pass
    
    def get_all_alerts(self):
        """Get all alerts history"""
        return self.alerts_history
    
    def get_recent_alerts(self, count=10):
        """Get recent alerts"""
        return self.alerts_history[-count:] if self.alerts_history else []

# Create a global alert manager instance
alert_manager = AlertManager()

# Test the alert manager
if __name__ == "__main__":
    print("Testing Alert Manager...")
    
    test_alerts = [
        ("Unauthorized Access", "Multiple failed logins from IP 192.168.1.100", "HIGH", "192.168.1.100"),
        ("Port Scan", "Port scanning detected on network", "MEDIUM", "10.0.0.50"),
        ("System Update", "Security patches available", "LOW", None),
        ("Malware Detected", "Malicious file found on server", "CRITICAL", "203.0.113.5")
    ]
    
    for title, desc, severity, ip in test_alerts:
        alert_manager.create_alert(title, desc, severity, ip)
        print("")
    
    print(f"Total alerts created: {alert_manager.alert_count}")
