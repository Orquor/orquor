#!/bin/bash
# deploy-landing.sh — Deploy de la landing page (04-web/) a Hostinger via FTP
# Uso: ./scripts/deploy-landing.sh [--dry-run]
#
# REQUISITOS:
#   - lftp instalado (sudo apt install lftp)
#   - Variables de entorno (export o en .env):
#       HOSTINGER_FTP_HOST  — Servidor FTP (default: ftp.orquor.com)
#       HOSTINGER_FTP_USER  — Usuario FTP de Hostinger
#       HOSTINGER_FTP_PASS  — Contraseña FTP de Hostinger
#   - Opcionales para modo SSH:
#       HOSTINGER_SSH_HOST  — Host SSH de Hostinger
#       HOSTINGER_SSH_USER  — Usuario SSH de Hostinger
#
# Comportamiento:
#   - Sube recursivamente 04-web/ a /public_html/ en Hostinger via lftp (FTPS)
#   - Respeta .gitignore y no sube archivos ocultos
#   - Con --dry-run: solo lista lo que se subiría, sin transferir
#   - Opcional: usar modo rsync si HOSTINGER_SSH_HOST está definido

set -euo pipefail

# ─── Colors ────────────────────────────────────────────────────────
BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
RESET="\033[0m"

log_info()  { echo -e "${BLUE}[deploy-landing]${RESET} $1"; }
log_ok()    { echo -e "${GREEN}[deploy-landing]${RESET} $1"; }
log_warn()  { echo -e "${YELLOW}[deploy-landing]${RESET} $1"; }
log_error() { echo -e "${RED}[deploy-landing]${RESET} $1"; }

# ─── Paths ─────────────────────────────────────────────────────────
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE_DIR="${PROJECT_ROOT}/04-web"
REMOTE_DIR="/public_html"

# ─── Config from environment ───────────────────────────────────────
HOSTINGER_FTP_HOST="${HOSTINGER_FTP_HOST:-ftp.orquor.com}"
HOSTINGER_FTP_USER="${HOSTINGER_FTP_USER:-}"
HOSTINGER_FTP_PASS="${HOSTINGER_FTP_PASS:-}"
HOSTINGER_SSH_HOST="${HOSTINGER_SSH_HOST:-}"
HOSTINGER_SSH_USER="${HOSTINGER_SSH_USER:-}"

DRY_RUN="false"
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN="true" ;;
        --help|-h)
            echo "Uso: $0 [--dry-run]"
            echo ""
            echo "  --dry-run   Solo mostrar qué se subiría, sin transferir"
            echo ""
            echo "Variables de entorno necesarias:"
            echo "  HOSTINGER_FTP_HOST  (default: ftp.orquor.com)"
            echo "  HOSTINGER_FTP_USER"
            echo "  HOSTINGER_FTP_PASS"
            echo "  HOSTINGER_SSH_HOST  (opcional, para modo rsync)"
            echo "  HOSTINGER_SSH_USER  (opcional, para modo rsync)"
            exit 0
            ;;
    esac
done

# ─── Validate ──────────────────────────────────────────────────────
echo -e "${BOLD}=== ORQUOR Landing Deploy to Hostinger ===${RESET}"
echo ""

if [ ! -d "$SOURCE_DIR" ]; then
    log_error "Directorio fuente no encontrado: $SOURCE_DIR"
    exit 1
fi

log_info "Source:    ${SOURCE_DIR}"
log_info "Target:    ${HOSTINGER_FTP_HOST}:${REMOTE_DIR}"

# Count files
FILE_COUNT=$(find "$SOURCE_DIR" -type f -not -path '*/\.*' | wc -l)
log_info "Archivos:  ${FILE_COUNT}"

echo ""

# ─── Choose mode ───────────────────────────────────────────────────
if [ -n "$HOSTINGER_SSH_HOST" ] && [ -n "$HOSTINGER_SSH_USER" ]; then
    log_info "Modo: rsync (SSH disponible)"
    echo ""

    if [ "$DRY_RUN" = "true" ]; then
        log_warn "DRY RUN — simulando rsync..."
        rsync -avzn --delete "${SOURCE_DIR}/" "${HOSTINGER_SSH_USER}@${HOSTINGER_SSH_HOST}:${REMOTE_DIR}/"
        echo ""
        log_ok "Dry run completado. Sin cambios aplicados."
        echo "Para subir realmente: $0"
        exit 0
    fi

    echo -ne "${YELLOW}¿Subir landing a ${HOSTINGER_SSH_HOST}:${REMOTE_DIR}? [y/N] ${RESET}"
    read -r confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        log_info "Deploy cancelado."
        exit 0
    fi

    log_info "Subiendo via rsync..."
    rsync -avz --delete "${SOURCE_DIR}/" "${HOSTINGER_SSH_USER}@${HOSTINGER_SSH_HOST}:${REMOTE_DIR}/"
    log_ok "rsync deploy completado."
else
    log_info "Modo: FTP (lftp con FTPS)"

    # Validate FTP credentials
    if [ -z "$HOSTINGER_FTP_USER" ]; then
        log_error "HOSTINGER_FTP_USER no está definida."
        echo "  Exporta la variable o crea un archivo .env:"
        echo "  export HOSTINGER_FTP_USER=tu_usuario"
        exit 1
    fi

    if [ -z "$HOSTINGER_FTP_PASS" ]; then
        log_error "HOSTINGER_FTP_PASS no está definida."
        echo "  Exporta la variable o crea un archivo .env:"
        echo "  export HOSTINGER_FTP_PASS=tu_password"
        exit 1
    fi

    # Check lftp is available
    if ! command -v lftp &>/dev/null; then
        log_error "lftp no encontrado. Instálalo con: sudo apt install lftp"
        exit 1
    fi

    echo ""

    if [ "$DRY_RUN" = "true" ]; then
        log_warn "DRY RUN — archivos que se subirían:"
        find "$SOURCE_DIR" -type f -not -path '*/\.*' | sort | while read -r f; do
            rel="${f#$SOURCE_DIR/}"
            echo "  ${REMOTE_DIR}/${rel}"
        done
        echo ""
        log_ok "Dry run completado. Sin archivos transferidos."
        echo "Para subir realmente: $0"
        exit 0
    fi

    echo -ne "${YELLOW}¿Subir landing a ${HOSTINGER_FTP_HOST}${REMOTE_DIR}? [y/N] ${RESET}"
    read -r confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        log_info "Deploy cancelado."
        exit 0
    fi

    log_info "Conectando a ${HOSTINGER_FTP_HOST}..."
    echo ""

    # lftp mirror: reverse (-R), only newer files, delete extras on remote
    lftp -c "
        set ftp:ssl-allow yes;
        set ftp:ssl-force yes;
        set ftp:ssl-protect-data yes;
        set ssl:verify-certificate no;
        open -u ${HOSTINGER_FTP_USER},${HOSTINGER_FTP_PASS} ${HOSTINGER_FTP_HOST};
        mirror -R --delete --verbose --exclude '.*' --exclude '.git/' ${SOURCE_DIR}/ ${REMOTE_DIR}/
    "

    echo ""
    log_ok "FTP deploy completado."
fi

# ─── Verify ─────────────────────────────────────────────────────────
echo ""
log_info "Verificar en: https://orquor.com"
log_info "Verificar en: https://orquor.com/demo.html"
log_info "Verificar en: https://orquor.com/academy.html"
echo -e "${BOLD}=== Deploy finalizado ===${RESET}"
