Alerting and Monitoring System
==============================

Implementation
--------------
- Real-time security alert processing
- Severity-based notification routing
- Slack integration (ready for webhook)
- Email notification system
- Alert history tracking

Severity Levels
---------------
- CRITICAL/HIGH: Immediate Slack + Email
- MEDIUM: Slack notification only  
- LOW/INFO: Logged only

API Endpoints
-------------
POST /api/add-detection - Create new alert
GET /api/security-alerts - Get alert history
GET /api/health - System status with alert metrics

Integration Points
------------------
- Slack: Set SLACK_WEBHOOK_URL environment variable
- Email: Set SMTP_SERVER, SMTP_USER, SMTP_PASSWORD
- Dashboard: Real-time alert display
- Logging: security_alerts.log file

Testing
-------
Run: python3 test_alerting.py
Or send POST to /api/add-detection with alert data

Configuration
-------------
For production:
export SLACK_WEBHOOK_URL="your_webhook"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_USER="your-email"
export SMTP_PASSWORD="your-password"

For demo:
System runs in simulation mode
