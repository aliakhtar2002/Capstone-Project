[PASTE THE ENTIRE CODE ABOVE]

@app.route('/api/alerts', methods=['POST'])
def receive_alert():
    """Endpoint that DVWA is actually sending to"""
    data = request.json
    print(f"[API] Alert received: {data}")
    
    # Format for your detection system
    detection = {
        'id': len(detections) + 1,
        'event_type': data.get('attack_type', 'unknown'),
        'ip_address': data.get('ip', request.remote_addr),
        'severity': 'high',
        'timestamp': datetime.now().isoformat(),
        'payload': data.get('payload', '')
    }
    
    detections.append(detection)
    
    return jsonify({'status': 'success', 'message': 'Alert received'}), 200
