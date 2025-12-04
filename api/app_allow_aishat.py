from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": ["https://3.145.146.136:8080"],
        "methods": ["*"],
        "allow_headers": ["*"],
        "supports_credentials": True
    }
})

@app.route('/api/security-alerts')
def alerts():
    return jsonify({
        "alerts": [{"id": 1, "message": "Test alert"}],
        "status": "aishat_allowed"
    })

@app.route('/api/data')
def data():
    return jsonify({
        "metrics": {"cpu": 45, "memory": 78},
        "events": ["event1", "event2"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
