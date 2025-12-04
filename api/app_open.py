from flask import Flask, jsonify
app = Flask(__name__)
@app.after_request
def cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
@app.route('/api/security-alerts')
def alerts():
    return jsonify({"alerts": []})
app.run(host='0.0.0.0', port=5000)
