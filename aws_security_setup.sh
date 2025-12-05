#!/bin/bash
# AWS Security Group Automation
# Sets up proper ports for SOC system

echo "Setting up AWS Security Group for SOC..."

PORTS="22 80 443 5000 8080"
SECURITY_GROUP_ID="sg-08ff165997ef7af8e"  # Your launch-wizard-4 group

for PORT in $PORTS; do
    echo "Checking port $PORT..."
    
    # Check if rule exists
    if ! aws ec2 describe-security-groups \
        --group-ids $SECURITY_GROUP_ID \
        --query "SecurityGroups[0].IpPermissions[?FromPort==\`$PORT\`]" \
        --output text | grep -q $PORT; then
        
        echo "Adding port $PORT to security group..."
        aws ec2 authorize-security-group-ingress \
            --group-id $SECURITY_GROUP_ID \
            --protocol tcp \
            --port $PORT \
            --cidr 0.0.0.0/0
    else
        echo "Port $PORT already open"
    fi
done

echo "Security group setup complete"
echo "Open ports: 22 (SSH), 80 (HTTP), 443 (HTTPS), 5000 (API), 8080 (Services)"
