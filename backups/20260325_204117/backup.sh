#!/bin/bash
BACKUP_DIR=~/backups/$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

echo "Backing up to $BACKUP_DIR..."

# Your personal files
cp -r ~/api $BACKUP_DIR/ 2>/dev/null
cp -r ~/mytest $BACKUP_DIR/ 2>/dev/null
cp ~/*.md $BACKUP_DIR/ 2>/dev/null
cp ~/*.py $BACKUP_DIR/ 2>/dev/null
cp ~/*.sh $BACKUP_DIR/ 2>/dev/null

# Teammates' files from Capstone-Project
cp -r ~/Capstone-Project $BACKUP_DIR/ 2>/dev/null

echo "Backup complete! Files saved to: $BACKUP_DIR"
echo "Total size: $(du -sh $BACKUP_DIR | cut -f1)"
