from flask import Flask, jsonify
from elasticsearch import Elasticsearch
from datetime import datetime

app = Flask(__name__)

# Try different Elasticsearch versions
try:
    # For elasticsearch 8.x
    es = Elasticsearch(['http://localhost:443'])
except:
    try:
        # For older versions
        from elasticsearch import Elasticsearch as ES
        es = ES(['http://localhost:443'])
    except:
        es = None

@app.route('/')
def home():
    if not es:
        return "<h1>Error: Cannot connect to Elasticsearch</h1>"
    
    try:
        # Get basic info
        info = es.info()
        count = es.count(index='security-events')['count']
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Elasticsearch Dashboard</title>
            <style>
                body {{ background: #0f172a; color: white; padding: 20px; font-family: Arial; }}
                .header {{ background: #1e293b; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
                .stats {{ display: flex; gap: 20px; margin-bottom: 20px; }}
                .stat-card {{ background: #334155; padding: 15px; border-radius: 8px; text-align: center; flex: 1; }}
                .stat-value {{ font-size: 24px; font-weight: bold; }}
                .events {{ background: #1e293b; padding: 20px; border-radius: 10px; }}
                .event {{ border-left: 4px solid; padding: 10px; margin: 5px 0; background: #2d3748; }}
                .critical {{ border-color: #ef4444; }}
                .high {{ border-color: #f97316; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Elasticsearch Dashboard</h1>
                <p>Elasticsearch Version: {info['version']['number']}</p>
                <p>Total Events: {count}</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value" style="color:#ef4444">{count}</div>
                    <div>Total Attacks</div>
                </div>
            </div>
            
            <div class="events">
                <h3>Recent Attacks:</h3>
                <p>Elasticsearch is running on port 443</p>
                <p>Dashboard is running on port 8081</p>
            </div>
        </body>
        </html>
        """
        return html
        
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

@app.route('/api/stats')
def stats():
    if not es:
        return jsonify({"error": "No Elasticsearch connection"})
    
    try:
        count = es.count(index='security-events')['count']
        return jsonify({
            "total_attacks": count,
            "elasticsearch": "running",
            "port": 443,
            "dashboard_port": 8081
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/test')
def test():
    """Test endpoint"""
    return jsonify({"status": "ok", "message": "Dashboard is running"})

if __name__ == '__main__':
    print("🚀 Starting Elasticsearch Dashboard...")
    print("📡 Elasticsearch: http://localhost:443")
    print("📊 Dashboard: http://0.0.0.0:8081")
    print("🔧 Press Ctrl+C to stop")
    
    try:
        app.run(host='0.0.0.0', port=8081, debug=False)
    except Exception as e:
        print(f"Error starting dashboard: {e}")
        print("Trying port 8082...")
        app.run(host='0.0.0.0', port=8082, debug=False)
