#!/bin/bash

# Configure Elasticsearch to use S3 for snapshots
curl -X PUT "localhost:9200/_snapshot/cyberpulse_backups" -H 'Content-Type: application/json' -d'
{
  "type": "s3",
  "settings": {
    "bucket": "cyberpulse-backups-grishab",
    "region": "us-east-2"
  }
}
'

# Create the first snapshot
curl -X PUT "localhost:9200/_snapshot/cyberpulse_backups/snapshot_1?wait_for_completion=true"

echo "Backup system configured!"
