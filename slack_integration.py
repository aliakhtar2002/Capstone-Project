#!/usr/bin/env python3
# Slack integration for SOC alerts

import os
import requests
import json

class SlackNotifier:
    def __init__(self, webhook_url=None):
        # Use environment variable or provided URL
        self.webhook_url = webhook_url or os.getenv('SLACK_WEBHOOK_URL', '')
        
        # If no webhook, we'll simulate
        self.simulation_mode = not self.webhook_url
        
        if self.simulation_mode:
            print("SlackNotifier: Running in simulation mode (no webhook configured)")
            print("To use real Slack, set SLACK_WEBHOOK_URL environment variable")
    
    def send_alert(self, alert_data):
        """Send alert to Slack"""
        if self.simulation_mode:
            return self._simulate_send(alert_data)
        else:
            return self._real_send(alert_data)
    
    def _real_send(self, alert_data):
        """Send actual Slack message"""
        try:
            # Format Slack message
            severity = alert_data.get('severity', 'UNKNOWN')
            color = self._get_color_for_severity(severity)
            
            slack_message = {
                "attachments": [{
                    "color": color,
                    "title": f"SOC Alert: {alert_data.get('event_type', 'Unknown')}",
                    "text": alert_data.get('description', ''),
                    "fields": [
                        {
                            "title": "Severity",
                            "value": severity,
                            "short": True
                        },
                        {
                            "title": "Source IP",
                            "value": alert_data.get('source_ip', 'Unknown'),
                            "short": True
                        },
                        {
                            "title": "Alert ID",
                            "value": str(alert_data.get('id', '')),
                            "short": True
                        }
                    ],
                    "footer": "CyberPulse SOC",
                    "ts": self._get_timestamp()
                }]
            }
            
            response = requests.post(
                self.webhook_url,
                json=slack_message,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "message": "Sent to Slack"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to send to Slack"
            }
    
    def _simulate_send(self, alert_data):
        """Simulate sending to Slack (for testing)"""
        severity = alert_data.get('severity', 'UNKNOWN')
        
        print(f"[SLACK SIMULATION] Alert would be sent to Slack:")
        print(f"  Title: SOC Alert - {alert_data.get('event_type')}")
        print(f"  Severity: {severity}")
        print(f"  Description: {alert_data.get('description')}")
        print(f"  Source IP: {alert_data.get('source_ip')}")
        
        # Simulate success
        return {
            "success": True,
            "simulated": True,
            "message": "Simulated Slack notification"
        }
    
    def _get_color_for_severity(self, severity):
        """Get Slack message color based on severity"""
        colors = {
            "CRITICAL": "#ff0000",  # Red
            "HIGH": "#ff6600",      # Orange
            "MEDIUM": "#ffcc00",    # Yellow
            "LOW": "#00cc00",       # Green
            "INFO": "#cccccc"       # Gray
        }
        return colors.get(severity.upper(), "#cccccc")
    
    def _get_timestamp(self):
        """Get current timestamp for Slack"""
        from datetime import datetime
        import time
        return time.mktime(datetime.now().timetuple())

# Test the Slack integration
if __name__ == "__main__":
    print("Testing Slack Integration...")
    print("="*50)
    
    notifier = SlackNotifier()
    
    test_alerts = [
        {
            "id": 1,
            "event_type": "unauthorized_access",
            "source_ip": "192.168.1.100",
            "description": "Multiple failed login attempts detected",
            "severity": "HIGH"
        },
        {
            "id": 2,
            "event_type": "port_scan",
            "source_ip": "10.0.0.50",
            "description": "Port scanning activity detected",
            "severity": "MEDIUM"
        }
    ]
    
    for alert in test_alerts:
        print(f"\nSending alert {alert['id']}:")
        result = notifier.send_alert(alert)
        print(f"Result: {result}")
    
    print("\n" + "="*50)
    print("To use real Slack integration:")
    print("1. Create Slack webhook at: https://api.slack.com/apps")
    print("2. Set environment variable: export SLACK_WEBHOOK_URL=your_webhook_url")
    print("3. Restart the SOC system")
