#!/usr/bin/env python3
"""
aishat_backend.py - Backend server for Aishat's dashboard
Connects her frontend to Elasticsearch on port 443
Run: python aishat_backend.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import json
import traceback

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# ===================== CONFIGURATION =====================
ELASTICSEARCH_HOST = "http://localhost:443"  # YOUR Elasticsearch
INDEX_NAME = "security-events"

# Connect to Elasticsearch
try:
    es = Elasticsearch([ELASTICSEARCH_HOST])
    print(f"✅ Connected to Elasticsearch at {ELASTICSEARCH_HOST}")
except Exception as e:
    print(f"❌ Failed to connect to Elasticsearch: {e}")
    es = None

# In-memory storage for blocked IPs (for demo)
blocked_ips = {}  # {ip: {ip: "1.2.3.4", blockedAt: "...", reason: "...", eventCount: 5}}
unblocked_history = []

# ===================== HELPER FUNCTIONS =====================
def format_event_for_frontend(hit):
    """Convert Elasticsearch event to Aishat's frontend format"""
    event = hit['_source']
    
    # Parse timestamp
    timestamp = event.get('@timestamp') or event.get('timestamp') or datetime.now().isoformat()
    try:
        formatted_time = datetime.fromisoformat(timestamp.replace('Z', '')).strftime('%Y-%m-%d %H:%M:%S')
    except:
        formatted_time = timestamp
    
    # Determine severity for frontend
    severity_map = {
        'critical': 'Critical',
        'high': 'Warning', 
        'medium': 'Warning',
        'low': 'Normal',
        'warning': 'Warning',
        'normal': 'Normal'
    }
    frontend_severity = severity_map.get(event.get('severity', '').lower(), 'Warning')
    
    # Map event types
    event_type = event.get('event_type', 'Unknown')
    if 'failed' in event_type.lower() or 'brute' in event_type.lower():
        frontend_event_type = 'Failed Login'
    elif 'success' in event_type.lower():
        frontend_event_type = 'Successful Login'
    else:
        frontend_event_type = event_type
    
    return {
        'id': hit['_id'],
        'time': formatted_time,
        'ip': event.get('source_ip', 'Unknown'),
        'username': event.get('username', 'Unknown'),
        'eventType': frontend_event_type,
        'severity': frontend_severity,
        'source': event.get('analyst', 'External')
    }

def get_event_count_for_ip(ip_address):
    """Count how many events from this IP"""
    if not es:
        return 1
    
    try:
        response = es.count(
            index=INDEX_NAME,
            body={"query": {"term": {"source_ip": ip_address}}}
        )
        return response['count']
    except:
        return 1

# ===================== API ENDPOINTS =====================

@app.route('/api/events', methods=['GET'])
def get_security_events():
    """Get all security events for Aishat's dashboard"""
    if not es:
        return jsonify([{
            "id": "error",
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "ip": "0.0.0.0",
            "username": "System",
            "eventType": "Elasticsearch Error",
            "severity": "Critical",
            "source": "Backend"
        }])
    
    try:
        # Query Elasticsearch
        response = es.search(
            index=INDEX_NAME,
            body={
                "query": {"match_all": {}},
                "sort": [{"@timestamp": {"order": "desc"}}],
                "size": 100
            }
        )
        
        # Format events for frontend
        events = []
        for hit in response['hits']['hits']:
            events.append(format_event_for_frontend(hit))
        
        return jsonify(events)
        
    except Exception as e:
        print(f"Error reading events: {traceback.format_exc()}")
        return jsonify([]), 500

@app.route('/api/events', methods=['POST'])
def add_security_event():
    """Add new event (for Waad & Victoria to send attacks)"""
    if not es:
        return jsonify({"error": "Elasticsearch not connected"}), 500
    
    try:
        event_data = request.json
        
        # Add metadata
        if 'timestamp' not in event_data:
            event_data['timestamp'] = datetime.now().isoformat()
        if '@timestamp' not in event_data:
            event_data['@timestamp'] = datetime.now().isoformat()
        
        # Store in Elasticsearch
        response = es.index(index=INDEX_NAME, document=event_data)
        
        return jsonify({
            "status": "success",
            "id": response['_id'],
            "message": "Event stored in Elasticsearch",
            "database": "Grishab's Elasticsearch"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/blocked', methods=['GET'])
def get_blocked_ips():
    """Get currently blocked IPs"""
    return jsonify(list(blocked_ips.values()))

@app.route('/api/unblocked', methods=['GET'])
def get_unblocked_ips():
    """Get unblocked IP history"""
    return jsonify(unblocked_history)

@app.route('/api/block', methods=['POST'])
def block_ip():
    """Block an IP address"""
    data = request.json
    ip_address = data.get('ip')
    reason = data.get('reason', 'Multiple failed login attempts')
    
    if not ip_address:
        return jsonify({"error": "IP address required"}), 400
    
    # Check if already blocked
    if ip_address in blocked_ips:
        return jsonify({"status": "already_blocked", "ip": ip_address}), 200
    
    # Count events from this IP
    event_count = get_event_count_for_ip(ip_address)
    
    # Add to blocked list
    blocked_info = {
        'ip': ip_address,
        'blockedAt': datetime.now().isoformat(),
        'reason': reason,
        'eventCount': event_count
    }
    blocked_ips[ip_address] = blocked_info
    
    print(f"🔒 Blocked IP: {ip_address} ({reason})")
    return jsonify({"status": "blocked", "ip": ip_address})

@app.route('/api/unblock', methods=['POST'])
def unblock_ip():
    """Unblock an IP address"""
    data = request.json
    ip_address = data.get('ip')
    
    if not ip_address:
        return jsonify({"error": "IP address required"}), 400
    
    # Check if actually blocked
    if ip_address not in blocked_ips:
        return jsonify({"error": "IP not blocked"}), 404
    
    # Move to unblocked history
    blocked_info = blocked_ips.pop(ip_address)
    blocked_info['unblockedAt'] = datetime.now().isoformat()
    unblocked_history.append(blocked_info)
    
    print(f"🔓 Unblocked IP: {ip_address}")
    return jsonify({"status": "unblocked", "ip": ip_address})

@app.route('/api/clear-blocks', methods=['POST'])
def clear_all_blocks():
    """Unblock all IPs"""
    unblocked_at = datetime.now().isoformat()
    
    # Move all blocked IPs to history
    for ip_address, info in list(blocked_ips.items()):
        info['unblockedAt'] = unblocked_at
        unblocked_history.append(info)
    
    blocked_ips.clear()
    
    print(f"🧹 Cleared all blocked IPs")
    return jsonify({"status": "cleared", "count": len(unblocked_history)})

@app.route('/api/stats', methods=['GET'])
def get_dashboard_stats():
    """Get statistics for Aishat's dashboard summary"""
    if not es:
        return jsonify({
            "total_events": 0,
            "failed_logins": 0,
            "brute_force_attempts": 0,
            "blocked_ips_count": len(blocked_ips),
            "source": "Backend (Elasticsearch offline)"
        })
    
    try:
        # Total events
        total_response = es.count(index=INDEX_NAME)
        total_events = total_response['count']
        
        # Failed logins count
        failed_response = es.count(
            index=INDEX_NAME,
            body={"query": {"term": {"event_type": "failed_login"}}}
        )
        failed_logins = failed_response.get('count', 0)
        
        # Brute force attempts
        brute_response = es.count(
            index=INDEX_NAME,
            body={"query": {"term": {"event_type": "brute_force"}}}
        )
        brute_force = brute_response.get('count', 0)
        
        # Events in last 24 hours
        yesterday = datetime.now() - timedelta(days=1)
        recent_response = es.count(
            index=INDEX_NAME,
            body={"query": {"range": {"@timestamp": {"gte": yesterday.isoformat()}}}}
        )
        recent_events = recent_response.get('count', 0)
        
        return jsonify({
            "total_events": total_events,
            "failed_logins": failed_logins,
            "brute_force_attempts": brute_force,
            "blocked_ips_count": len(blocked_ips),
            "recent_events": recent_events,
            "source": "Elasticsearch (Grishab's database)"
        })
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({
            "total_events": 0,
            "failed_logins": 0,
            "brute_force_attempts": 0,
            "blocked_ips_count": len(blocked_ips),
            "source": f"Error: {str(e)}"
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    es_status = "connected" if es else "disconnected"
    return jsonify({
        "status": "running",
        "elasticsearch": es_status,
        "blocked_ips": len(blocked_ips),
        "unblocked_history": len(unblocked_history),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/')
def index():
    """Welcome page"""
    return """
    <html>
    <body style="background:#0f172a; color:white; padding:30px; font-family:Arial;">
        <h1>🚀 Aishat's Dashboard Backend</h1>
        <p>Connected to Elasticsearch on port 443</p>
        <p>Endpoints:</p>
        <ul>
            <li><code>GET /api/events</code> - Get security events</li>
            <li><code>POST /api/events</code> - Add new event</li>
            <li><code>GET /api/stats</code> - Dashboard statistics</li>
            <li><code>GET /api/blocked</code> - Blocked IPs</li>
            <li><code>POST /api/block</code> - Block an IP</li>
            <li><code>POST /api/unblock</code> - Unblock an IP</li>
        </ul>
        <p><strong>Frontend:</strong> Use with Aishat's HTML dashboard</p>
        <p><strong>Database:</strong> Grishab's Elasticsearch (port 443)</p>
    </body>
    </html>
    """

# ===================== MAIN =====================
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AISHAT'S DASHBOARD BACKEND SERVER")
    print("="*60)
    print(f"📡 Elasticsearch: {ELASTICSEARCH_HOST}")
    print(f"🌐 API Server: http://0.0.0.0:5000")
    print(f"🔗 Frontend URL: http://<SERVER_IP>:8080")
    print("="*60)
    print("Endpoints:")
    print("  GET  /api/events     - Get security events")
    print("  POST /api/events     - Add new attack")
    print("  GET  /api/stats      - Dashboard statistics")
    print("  GET  /api/blocked    - Blocked IPs")
    print("  POST /api/block      - Block IP")
    print("  POST /api/unblock    - Unblock IP")
    print("="*60)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("Trying port 5001...")
        app.run(host='0.0.0.0', port=5001, debug=False)
