from flask import Flask, jsonify
app = Flask(__name__)
@app.after_request
def no_cors(response):
    response.headers['Access-Control-Allow-Origin'] = ''
    return response
@app.route('/api/security-alerts')
def alerts():
    return jsonify({"alerts": [], "access": "localhost_only"})
app.run(host='127.0.0.1', port=5000)
