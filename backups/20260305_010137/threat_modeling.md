# CyberPulse Threat Analysis
Ali Akhtar - CS Capstone

## What I Built
- Flask API on AWS EC2
- Endpoints for security data
- Gets data from Waad's scripts
- Sends data to Aishat's dashboard

## Security Issues I Found

### 1. No Login Required
- Problem: Anyone can send data to my API
- Risk: Fake attacks could be sent
- Fix: Add API keys

### 2. No Rate Limiting  
- Problem: Too many requests can crash API
- Risk: Denial of service attacks
- Fix: Limit requests per minute

### 3. Error Messages Show Too Much
- Problem: Errors show code details
- Risk: Hackers learn about system
- Fix: Generic error messages

### 4. Running in Debug Mode
- Problem: Debug mode on in production
- Risk: Security vulnerabilities
- Fix: Turn off debug mode

## Data Flow Security

Waad's Scripts -> My API -> Memory -> Dashboard
                                  -> Block Bad IPs

## What I Need to Fix First
1. Add API key check
2. Turn off debug mode  
3. Add request limits
4. Better error handling

## Notes
This is my first Flask API so I'm learning security as I go.
I'll fix these issues before final demo.
