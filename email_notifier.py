import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotifier:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', '')
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        
    def send_alert(self, alert_data):
        severity = alert_data.get('severity', 'UNKNOWN')
        
        if self.smtp_server and self.smtp_user:
            print(f"EMAIL: Sent {severity} alert")
            return {"status": "sent"}
        else:
            print(f"EMAIL SIM: {severity} alert simulated")
            return {"status": "simulated"}
