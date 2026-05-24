#!/bin/bash
# deploy-hostinger.sh — Deploy de ORQUOR a Hostinger
# Uso: ./deploy-hostinger.sh [ftp|ssh]
# Requiere: credenciales Hostinger en variables de entorno

set -e

PROJECT_DIR="/mnt/c/Users/frefe/OneDrive/Desktop/START UP/orquor"
DEPLOY_DIR="${PROJECT_DIR}/04-web"

# Config — setear en .env o export
HOSTINGER_FTP_HOST="${HOSTINGER_FTP_HOST:-ftp.orquor.com}"
HOSTINGER_FTP_USER="${HOSTINGER_FTP_USER:-}"
HOSTINGER_FTP_PASS="${HOSTINGER_FTP_PASS:-}"
HOSTINGER_SSH_HOST="${HOSTINGER_SSH_HOST:-}"
HOSTINGER_SSH_USER="${HOSTINGER_SSH_USER:-}"

MODE="${1:-ftp}"

echo "=== ORQUOR Deploy to Hostinger ==="
echo "Mode: ${MODE}"
echo "Source: ${DEPLOY_DIR}"

case "$MODE" in
    ftp)
        if [ -z "$HOSTINGER_FTP_PASS" ]; then
            echo "ERROR: HOSTINGER_FTP_PASS no definida. Exportala o crea .env"
            exit 1
        fi
        echo "Deploying via FTP..."
        # Usar lftp para upload recursivo
        lftp -c "set ftp:ssl-allow yes; open -u ${HOSTINGER_FTP_USER},${HOSTINGER_FTP_PASS} ${HOSTINGER_FTP_HOST}; mirror -R ${DEPLOY_DIR}/ /public_html/"
        echo "FTP deploy completado."
        ;;
    ssh)
        if [ -z "$HOSTINGER_SSH_HOST" ]; then
            echo "ERROR: HOSTINGER_SSH_HOST no definida"
            exit 1
        fi
        echo "Deploying via SSH/rsync..."
        rsync -avz --delete "${DEPLOY_DIR}/" "${HOSTINGER_SSH_USER}@${HOSTINGER_SSH_HOST}:~/public_html/"
        echo "SSH deploy completado."
        ;;
    *)
        echo "Uso: $0 [ftp|ssh]"
        exit 1
        ;;
esac

echo "=== Deploy finalizado ==="
echo "Verificar: https://orquor.com"
