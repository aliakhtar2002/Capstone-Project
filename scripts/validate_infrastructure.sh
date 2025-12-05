#!/bin/bash
# Validate SOC infrastructure setup

echo "======================================"
echo "  SOC Infrastructure Validation"
echo "======================================"
echo "Date: $(date)"
echo ""

# Check system
echo "1. System Check:"
echo "---------------"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "  OS: $NAME $VERSION"
else
    echo "  OS: Amazon Linux"
fi

echo "  Hostname: $(hostname)"
echo "  IP: $(curl -s ifconfig.me)"

# Check Docker
echo ""
echo "2. Docker Check:"
echo "---------------"
if command -v docker &> /dev/null; then
    echo "  Docker: Installed"
    docker --version | cut -d',' -f1
else
    echo "  Docker: NOT INSTALLED"
fi

if command -v docker-compose &> /dev/null; then
    echo "  Docker Compose: Installed"
    docker-compose --version
else
    echo "  Docker Compose: NOT INSTALLED"
fi

# Check ports
echo ""
echo "3. Port Check:"
echo "-------------"
ports_to_check=(22 80 443 5000 8080)
for port in "${ports_to_check[@]}"; do
    if ss -tuln | grep ":$port " > /dev/null; then
        echo "  Port $port: LISTENING"
    else
        echo "  Port $port: NOT LISTENING"
    fi
done

# Check project files
echo ""
echo "4. Project Check:"
echo "----------------"
required_files=("docker-compose.yml" "app.py" "deploy_infrastructure.sh")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  $file: PRESENT"
    else
        echo "  $file: MISSING"
    fi
done

echo ""
echo "======================================"
echo "         Validation Complete"
echo "======================================"
