from flask import Flask, jsonify
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": ["https://3.145.146.136:8080", "http://3.145.146.136:8080"],
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH", "HEAD"],
        "allow_headers": ["*"],
        "expose_headers": ["*"],
        "supports_credentials": True,
        "max_age": 86400
    }
})

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://3.145.146.136:8080')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, Accept')
    response.headers.add('Access-Control-Expose-Headers', '*')
    return response

@app.route('/')
def home():
    return jsonify({"status": "CORS fixed", "aishat_domain": "allowed"})

@app.route('/api/security-alerts')
def alerts():
    return jsonify({"alerts": [], "cors": "enabled_for_aishat"})

@app.route('/api/test')
def test():
    return jsonify({"message": "CORS should work now"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
