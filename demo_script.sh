#!/bin/bash
echo "=== CYBERPULSE DEMO ==="
echo "1. API Health:"
curl -s http://localhost:5000/api/health | python3 -m json.tool
echo ""
echo "2. Current Detections:"
curl -s http://localhost:5000/api/security-events | python3 -m json.tool | head -20
echo ""
echo "3. Send Test Attack:"
curl -s -X POST http://localhost:5000/api/add-detection \
  -H "Content-Type: application/json" \
  -d '{"event_type":"demo_attack","ip_address":"10.0.0.99","severity":"critical"}' | python3 -m json.tool
echo ""
echo "4. Verify Attack Received:"
curl -s http://localhost:5000/api/health | grep detections_count
echo ""
echo "5. Your Dashboard: http://3.145.146.136:8081/soc-dashboard.html"
echo "6. Backup Just Ran: $(ls -la ~/backups/ | tail -1)"
echo "7. SAST Report: $(cat ~/sast_report.json | head -10)"
