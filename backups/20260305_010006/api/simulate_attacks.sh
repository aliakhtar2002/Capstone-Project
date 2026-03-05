#!/bin/bash
echo "Simulating attacks to API..."

# Simulate brute force
curl -s -X POST http://localhost:5000/api/add-detection \
  -H "Content-Type: application/json" \
  -d '{"event_type":"brute_force","ip_address":"10.0.0.1","severity":"critical"}'

# Simulate SQL injection  
curl -s -X POST http://localhost:5000/api/add-detection \
  -H "Content-Type: application/json" \
  -d '{"event_type":"sql_injection","ip_address":"10.0.0.2","severity":"high"}'

# Simulate port scan
curl -s -X POST http://localhost:5000/api/add-detection \
  -H "Content-Type: application/json" \
  -d '{"event_type":"port_scan","ip_address":"10.0.0.3","severity":"medium"}'

echo -e "\n\n✅ Attacks sent! Current detections:"
curl http://localhost:5000/api/security-events | python3 -m json.tool
