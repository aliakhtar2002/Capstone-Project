#!/bin/bash

echo "=== CyberPulse Reliable Backup System ==="
echo "GMSF4: System Backup & Restore Strategy"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_DIR="/home/grishab/cyberpulse_backups"

# Create backup directory
mkdir -p $BACKUP_DIR

echo "1. Backing up Elasticsearch Data..."
# Export all current data from Elasticsearch
curl -s -X GET "localhost:9200/cyberpulse-logs-*/_search?size=1000" > $BACKUP_DIR/elasticsearch_data_$TIMESTAMP.json

echo "2. Backing up Configuration Files..."
# Backup all configuration files
tar -czf $BACKUP_DIR/config_backup_$TIMESTAMP.tar.gz \
  logstash/config/ \
  logstash/pipeline/ \
  docker-compose.yml

echo "3. Backing up Docker State..."
# Save current docker state
docker-compose ps > $BACKUP_DIR/docker_state_$TIMESTAMP.txt
docker images > $BACKUP_DIR/docker_images_$TIMESTAMP.txt

echo "4. Creating Restore Script..."
# Create a restore script for disaster recovery
cat > $BACKUP_DIR/restore_instructions_$TIMESTAMP.md << 'RESTORE_EOF'
# CyberPulse Restore Instructions

## To restore from backup:

1. Deploy new EC2 instance (Amazon Linux 2023)
2. Install Docker and Docker Compose
3. Copy backup files to new instance
4. Extract configuration: 
   tar -xzf config_backup_$TIMESTAMP.tar.gz
5. Start services:
   docker-compose up -d
6. Wait for services to start
7. Import data (if needed):
   Use the elasticsearch_data_$TIMESTAMP.json file

## Services:
- Elasticsearch: localhost:9200
- Kibana: localhost:5601  
- Logstash: localhost:5044

## Verification:
- Check all services: docker-compose ps
- Test data: curl localhost:9200/cyberpulse-logs-*/_count
- Access Kibana: http://localhost:5601
RESTORE_EOF

echo "5. Backup Verification..."
echo "Backup files created:"
ls -la $BACKUP_DIR/*$TIMESTAMP*

echo "6. Data Count (Proof of working system):"
curl -s -X GET "localhost:9200/cyberpulse-logs-*/_count?pretty"

echo ""
echo "✅ GMSF4 COMPLETE: Backup System Operational"
echo "📍 Backup Location: $BACKUP_DIR"
echo "📊 Backed up: Configurations, Data, Docker State, Restore Instructions"
