#!/bin/bash
# One-click SOC setup for EC2

echo "=== CyberPulse SOC One-Click Setup ==="

# Check if on EC2
if [ ! -f /sys/hypervisor/uuid ] && [ ! -d /sys/bus/vmware/devices ]; then
    echo "ERROR: Not running on EC2"
    exit 1
fi

# Run setup
./automate_ec2_setup.sh

# Show success
echo ""
echo "========================================"
echo "SOC SETUP COMPLETE"
echo "========================================"
echo "What was installed:"
echo "1. Docker & Docker Compose"
echo "2. SOC project from GitHub"
echo "3. All dependencies"
echo "4. Running services"
echo ""
echo "Access:"
echo "- API: http://$(curl -s ifconfig.me):5000"
echo "- Health: curl http://localhost:5000/api/health"
echo "- Alerts: curl http://localhost:5000/api/security-alerts"
echo ""
echo "To configure alerts:"
echo "Edit app.py or set environment variables"
echo "========================================"
