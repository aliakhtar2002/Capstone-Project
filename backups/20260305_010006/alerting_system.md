# Alerting & Monitoring System
Ali Akhtar - AAL8 & AALSF4

## Features Implemented:
✅ Real-time security alerts  
✅ Severity-based notifications  
✅ Console alert logging  
✅ Slack webhook integration (ready)  
✅ Email alert simulation  
✅ Alert history endpoint  

## Alert Triggers:
- HIGH/CRITICAL severity: Immediate alerts + automated blocking
- MEDIUM severity: Security alerts only  
- LOW severity: Logged, no alerts

## Endpoints:
- POST /api/detections - Triggers automated alerts
- GET /api/security-alerts - Returns alert history
- GET /api/health - Includes alert metrics

## Integration Ready:
- Slack webhooks configured in code
- Email system placeholder added
- Console logging for demo purposes

## Evidence:
- security_alerts array stores all alerts
- Automated IP blocking with alerts
- Real-time console notifications
