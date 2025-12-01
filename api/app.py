from flask import Flask, jsonify, request
from datetime import datetime
import requests
import json

app = Flask(__name__)

detections = []
blocked_ips = []
security_alerts = []

def send_slack_alert(severity, message, detection_data):
    """AALSF4 - Slack notification integration"""
    alert = {
        'timestamp': datetime.now().isoformat(),
        'severity': severity,
        'message': message,
        'detection': detection_data
    }
    security_alerts.append(alert)
    
    # Print alert to console (AAL8)
    print(f"🚨 SECURITY ALERT [{severity.upper()}]: {message}")
    print(f"   Detection: {detection_data.get('event_type')} from {detection_data.get('ip_address')}")
    print(f"   Time: {alert['timestamp']}")
    
    # In production, this would send to Slack webhook
    # slack_webhook = "https://hooks.slack.com/services/..."
    # requests.post(slack_webhook, json={"text": f"🚨 {message}"})
    
    return alert

def send_email_alert(severity, message):
    """AALSF4 - Email notification simulation"""
    print(f"📧 EMAIL ALERT: {severity} - {message}")
    # In production: smtplib or AWS SES
    
@app.route('/api/security-events')
def get_security_events():
    return jsonify({
        'status': 'success',
        'data': detections,
        'count': len(detections)
    })

@app.route('/api/detection-stats')
def get_detection_stats():
    stats = {
        'total_attacks': len(detections),
        'critical_count': len([d for d in detections if d.get('severity') == 'critical']),
        'high_count': len([d for d in detections if d.get('severity') == 'high']),
        'medium_count': len([d for d in detections if d.get('severity') == 'medium']),
        'last_updated': datetime.now().isoformat()
    }
    return jsonify(stats)

@app.route('/api/add-detection', methods=['POST'])
def add_detection():
    data = request.json
    detection = {
        'id': len(detections) + 1,
        'event_type': data.get('event_type', 'unknown'),
        'ip_address': data.get('ip_address', '0.0.0.0'),
        'severity': data.get('severity', 'medium'),
        'timestamp': datetime.now().isoformat()
    }
    detections.append(detection)
    
    return jsonify({
        'status': 'success', 
        'message': 'Detection added',
        'detection_id': detection['id']
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'detections_count': len(detections),
        'alerts_count': len(security_alerts),
        'blocked_ips_count': len(blocked_ips)
    })

@app.route('/api/dashboard/stats')
def get_dashboard_stats():
    return jsonify({
        'total_attacks_today': len(detections),
        'blocked_ips': len(blocked_ips),
        'active_threats': len([d for d in detections if d.get('severity') == 'critical']),
        'false_positives': len([d for d in detections if d.get('severity') == 'low']),
        'alerts_generated': len(security_alerts),
        'system_status': 'operational',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/detections', methods=['GET', 'POST'])
def handle_detections():
    if request.method == 'GET':
        return jsonify({
            'status': 'success',
            'detections': detections,
            'count': len(detections)
        })
    elif request.method == 'POST':
        data = request.json
        detection = {
            'id': len(detections) + 1,
            'event_type': data.get('event_type', 'unknown'),
            'ip_address': data.get('ip_address', '0.0.0.0'),
            'severity': data.get('severity', 'medium'),
            'timestamp': datetime.now().isoformat(),
            'source': 'waad_detection'
        }
        detections.append(detection)
        
        # AAL8 & AALSF4 - Automated alerting based on severity
        if detection['severity'] in ['high', 'critical']:
            # Trigger alerts
            alert_message = f"High severity {detection['event_type']} detected from {detection['ip_address']}"
            send_slack_alert(detection['severity'], alert_message, detection)
            
            # Trigger automated response
            block_result = block_malicious_ip(detection['ip_address'], f"Automated block for {detection['event_type']}")
            detection['automated_action'] = block_result
            
        elif detection['severity'] == 'medium':
            alert_message = f"Medium severity event: {detection['event_type']} from {detection['ip_address']}"
            send_slack_alert('medium', alert_message, detection)
        
        return jsonify({
            'status': 'success', 
            'message': 'Detection received via /api/detections',
            'detection_id': detection['id'],
            'automated_action_taken': detection.get('automated_action', {}).get('status') if detection.get('automated_action') else None,
            'alert_generated': detection['severity'] in ['high', 'critical', 'medium']
        })

@app.route('/api/automated-response/block-ip', methods=['POST'])
def block_ip_endpoint():
    data = request.json
    ip_address = data.get('ip_address')
    reason = data.get('reason', 'Manual block request')
    
    result = block_malicious_ip(ip_address, reason)
    return jsonify(result)

@app.route('/api/blocked-ips')
def get_blocked_ips():
    return jsonify({
        'blocked_ips': blocked_ips,
        'count': len(blocked_ips)
    })

@app.route('/api/security-alerts')
def get_security_alerts():
    """AAL8 - Alert monitoring endpoint"""
    return jsonify({
        'alerts': security_alerts[-10:],  # Last 10 alerts
        'total_alerts': len(security_alerts),
        'high_severity_alerts': len([a for a in security_alerts if a.get('severity') in ['high', 'critical']])
    })

def block_malicious_ip(ip_address, reason):
    if ip_address in [ip['ip'] for ip in blocked_ips]:
        return {"status": "already_blocked", "message": f"IP {ip_address} already blocked"}
    
    blocked_ip = {
        'ip': ip_address,
        'reason': reason,
        'timestamp': datetime.now().isoformat(),
        'action': 'blocked'
    }
    blocked_ips.append(blocked_ip)
    
    print(f"🚫 AUTOMATED RESPONSE: Blocked IP {ip_address} - Reason: {reason}")
    
    # AALSF4 - Send alert for blocking action
    send_slack_alert('high', f"IP {ip_address} blocked automatically", {'action': 'ip_block', 'reason': reason})
    
    return {
        "status": "success",
        "action": f"Blocked IP {ip_address}",
        "reason": reason,
        "timestamp": datetime.now().isoformat(),
        "playbook": "block_ip"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
