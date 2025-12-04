from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "https://cyberpulse.com",
    "https://www.cyberpulse.com",
    "https://3.145.146.136:8080",
    "http://3.145.146.136:8080"
]

CORS(app, origins=ALLOWED_ORIGINS, 
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     supports_credentials=True,
     max_age=3600)

@app.before_request
def security_checks():
    client_ip = request.remote_addr
    origin = request.headers.get('Origin', '')
    app.logger.info(f"Request: {client_ip} -> {request.path} | Origin: {origin}")
    
    BLOCKED_IPS = [
        "216.247.106.78",
        "216.180.127.200",
        "45.145.155.14",
    ]
    
    if client_ip in BLOCKED_IPS:
        app.logger.warning(f"BLOCKED IP: {client_ip}")
        return jsonify({"error": "Access denied"}), 403

@app.route('/')
def index():
    return jsonify({
        "service": "CyberPulse API",
        "status": "active",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/security-alerts')
def security_alerts():
    return jsonify({
        "status": "success",
        "alerts": [
            {
                "id": 1,
                "type": "brute_force",
                "severity": "high",
                "message": "Attack blocked",
                "timestamp": datetime.utcnow().isoformat()
            },
            {
                "id": 2,
                "type": "api_access",
                "severity": "info",
                "message": "Dashboard connected",
                "timestamp": datetime.utcnow().isoformat()
            }
        ]
    })

@app.route('/api/dashboard-data')
def dashboard_data():
    return jsonify({
        "metrics": {
            "total_alerts": 15,
            "blocked_ips": 3,
            "active_threats": 2,
            "uptime": "99.8%"
        },
        "recent_events": [
            {"time": datetime.utcnow().isoformat(), "event": "Dashboard connected", "user": "aishat"},
            {"time": datetime.utcnow().isoformat(), "event": "API active", "status": "normal"}
        ]
    })

@app.route('/api/test-cors')
def test_cors():
    origin = request.headers.get('Origin', 'none')
    return jsonify({
        "cors_test": "success",
        "origin": origin,
        "allowed": origin in ALLOWED_ORIGINS,
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    print("Server starting: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
