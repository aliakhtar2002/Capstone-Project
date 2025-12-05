#!/bin/bash
# SOC EC2 Automation Script
# Run this on a fresh EC2 instance to set up everything automatically

echo "=== SOC EC2 Automation Setup ==="
echo "Start time: $(date)"
echo ""

# 1. System updates
echo "1. Updating system..."
sudo yum update -y

# 2. Install Docker
echo "2. Installing Docker..."
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# 3. Install Docker Compose
echo "3. Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Clone project
echo "4. Cloning SOC project..."
cd ~
git clone https://github.com/aliakhtar2002/Capstone-Project.git
cd Capstone-Project

# 5. Setup environment
echo "5. Setting up environment..."
mkdir -p logs backups

# 6. Create setup verification
echo "6. Verifying setup..."
docker --version
docker-compose --version
git --version

# 7. Start services
echo "7. Starting SOC services..."
docker-compose up -d

# 8. Final check
echo "8. Final verification..."
sleep 5
echo "Checking services:"
docker-compose ps

echo ""
echo "=== SETUP COMPLETE ==="
echo "API: http://$(curl -s ifconfig.me):5000"
echo "Check: curl http://localhost:5000/api/health"
echo ""
echo "For Slack/Email alerts:"
echo "export SLACK_WEBHOOK_URL=your_webhook"
echo "export SMTP_SERVER=smtp.gmail.com"
echo "export SMTP_USER=your_email"
echo "export SMTP_PASSWORD=your_password"
