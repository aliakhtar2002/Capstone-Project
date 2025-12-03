#!/bin/bash

echo "=== CyberPulse Backup System Setup ==="

# Step 1: Configure the backup repository
echo "1. Configuring backup repository..."
REPO_RESPONSE=$(curl -s -X PUT "localhost:9200/_snapshot/cyberpulse_backups" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/usr/share/elasticsearch/backups"
  }
}
')

if [[ "$REPO_RESPONSE" == *"acknowledged\"true"* ]]; then
    echo "✅ Backup repository configured successfully"
else
    echo "❌ Repository configuration failed: $REPO_RESPONSE"
    exit 1
fi

# Step 2: Create first backup
echo "2. Creating initial backup..."
BACKUP_RESPONSE=$(curl -s -X PUT "localhost:9200/_snapshot/cyberpulse_backups/first_backup?wait_for_completion=true")

if [[ "$BACKUP_RESPONSE" == *"accepted\"true"* ]] || [[ "$BACKUP_RESPONSE" == *"state\":\"SUCCESS"* ]]; then
    echo "✅ Initial backup created successfully"
else
    echo "⚠️ Backup response: $BACKUP_RESPONSE"
fi

# Step 3: Verify backup
echo "3. Verifying backup system..."
curl -s -X GET "localhost:9200/_snapshot/cyberpulse_backups/_all?pretty"

# Step 4: Check backup files on disk
echo "4. Backup files on disk:"
ls -la elasticsearch_backups/

echo "=== Backup System Ready ==="
