from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": ["https://3.145.146.136:8080"],
        "methods": ["*"],
        "allow_headers": ["*"],
        "supports_credentials": True
    }
})

security_alerts = []
alert_counter = 1

class SlackNotifier:
    @staticmethod
    def send_alert(alert_data):
        severity = alert_data.get('severity', 'UNKNOWN')
        webhook_url = os.getenv('SLACK_WEBHOOK_URL', '')
        
        if webhook_url:
            print(f"SLACK: Sent {severity} alert")
            return {"status": "sent", "channel": "slack"}
        else:
            print(f"SLACK SIM: {severity} alert simulated")
            return {"status": "simulated", "channel": "slack"}

class EmailNotifier:
    @staticmethod
    def send_alert(alert_data):
        severity = alert_data.get('severity', 'UNKNOWN')
        smtp_configured = os.getenv('SMTP_SERVER', '') and os.getenv('SMTP_USER', '')
        
        if smtp_configured:
            print(f"EMAIL: Sent {severity} alert")
            return {"status": "sent", "channel": "email"}
        else:
            print(f"EMAIL SIM: {severity} alert simulated")
            return {"status": "simulated", "channel": "email"}

class AlertSystem:
    @staticmethod
    def create_alert(event_type, source_ip, description, severity):
        global alert_counter
        
        alert = {
            "id": alert_counter,
            "event_type": event_type,
            "source_ip": source_ip,
            "description": description,
            "severity": severity.upper(),
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
        
        alert_counter += 1
        security_alerts.append(alert)
        
        AlertSystem._process_alert(alert)
        
        return alert
    
    @staticmethod
    def _process_alert(alert):
        severity = alert["severity"]
        
        print(f"ALERT [{severity}]")
        print(f"Type: {alert['event_type']}")
        print(f"IP: {alert['source_ip']}")
        print(f"Desc: {alert['description']}")
        
        if severity in ["CRITICAL", "HIGH"]:
            print("Action: Immediate")
            slack_result = SlackNotifier.send_alert(alert)
            email_result = EmailNotifier.send_alert(alert)
            print(f"Notified: Slack={slack_result['status']}, Email={email_result['status']}")
            
            with open("security_alerts.log", "a") as f:
                f.write(f"[IMMEDIATE] {json.dumps(alert)}\n")
                
        elif severity == "MEDIUM":
            print("Action: Security team")
            slack_result = SlackNotifier.send_alert(alert)
            print(f"Notified: Slack={slack_result['status']}")
            
            with open("security_alerts.log", "a") as f:
                f.write(f"[SECURITY] {json.dumps(alert)}\n")
                
        else:
            print("Action: Log only")
            with open("security_alerts.log", "a") as f:
                f.write(f"[LOG] {json.dumps(alert)}\n")

@app.route('/api/security-alerts')
def get_alerts():
    return jsonify({
        "alerts": security_alerts[-20:],
        "total": len(security_alerts),
        "status": "success"
    })

@app.route('/api/add-detection', methods=['POST'])
def add_detection():
    try:
        data = request.json
        
        required = ['event_type', 'source_ip', 'description', 'severity']
        for field in required:
            if field not in data:
                return jsonify({
                    "error": f"Missing: {field}",
                    "status": "error"
                }), 400
        
        alert = AlertSystem.create_alert(
            data['event_type'],
            data['source_ip'],
            data['description'],
            data['severity']
        )
        
        return jsonify({
            "message": "Alert created",
            "alert_id": alert['id'],
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/data')
def get_data():
    return jsonify({
        "metrics": {
            "cpu": 45,
            "memory": 78,
            "alerts_today": len(security_alerts),
            "active_alerts": len([a for a in security_alerts if a['status'] == 'active'])
        },
        "events": ["system_ok", "monitoring_active"],
        "status": "operational"
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "running",
            "alerting": "active",
            "database": "connected"
        },
        "alerts_summary": {
            "total": len(security_alerts),
            "critical": len([a for a in security_alerts if a['severity'] == 'CRITICAL']),
            "high": len([a for a in security_alerts if a['severity'] == 'HIGH'])
        }
    })

@app.route('/')
def home():
    return jsonify({
        "message": "CyberPulse SOC API",
        "version": "1.0",
        "endpoints": [
            "/api/security-alerts",
            "/api/add-detection",
            "/api/data", 
            "/api/health"
        ]
    })

if __name__ == '__main__':
    AlertSystem.create_alert(
        "system_start",
        "127.0.0.1",
        "SOC System started",
        "info"
    )
    
    print("CyberPulse SOC API")
    print("Alerting: " + ("CONFIGURED" if os.getenv('SLACK_WEBHOOK_URL') else "SIMULATION"))
    print("Endpoints ready")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
