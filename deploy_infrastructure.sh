#!/bin/bash
echo " Deploying CyberPulse SOC Infrastructure..."

# Update system
echo "Updating system packages..."
sudo yum update -y

# Install Docker
echo "Installing Docker..."
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create project structure
echo "Creating project directories..."
mkdir -p ~/cyberpulse/{api,database,scripts,logs}

# Copy API code
echo "Setting up API..."
cp -r ~/api/* ~/cyberpulse/api/

# Create Dockerfile for API
cat > ~/cyberpulse/api/Dockerfile << 'DOCKERFILE'
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
DOCKERFILE

# Create requirements file
echo "Flask==2.3.3" > ~/cyberpulse/api/requirements.txt
echo "psycopg2-binary==2.9.7" >> ~/cyberpulse/api/requirements.txt
echo "requests==2.31.0" >> ~/cyberpulse/api/requirements.txt

echo " Infrastructure deployment script ready!"
echo "Run './deploy_infrastructure.sh' to deploy"
