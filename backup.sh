#!/bin/bash
# backup-orquor.sh — Backup diario del proyecto a ~/backups/
BACKUP_DIR="/home/frefe/backups/orquor"
PROJECT="/mnt/c/Users/frefe/OneDrive/Desktop/START UP/orquor"
DATE=$(date +%Y%m%d_%H%M%S)
ARCHIVE="${BACKUP_DIR}/orquor_${DATE}.tar.gz"

mkdir -p "$BACKUP_DIR"

tar -czf "$ARCHIVE" \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='.pytest_cache' \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='.bridge_*' \
    --exclude='.screen.png' \
    -C "$(dirname "$PROJECT")" "$(basename "$PROJECT")" 2>/dev/null

echo "Backup: $ARCHIVE ($(stat -c%s "$ARCHIVE" 2>/dev/null || echo '?') bytes)"

# Rotación: mantener últimos 10 backups
ls -t "${BACKUP_DIR}"/orquor_*.tar.gz 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null
echo "Rotacion: $(ls "${BACKUP_DIR}"/orquor_*.tar.gz 2>/dev/null | wc -l) backups"
