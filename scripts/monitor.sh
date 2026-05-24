#!/bin/bash
# monitor.sh — Monitoreo de GPU, RAM, disco y envío de alertas
# Uso: ./scripts/monitor.sh [--once|--watch <seconds>|--alert-test]
#
# Monitorea:
#   - GPU (nvidia-smi): temperatura, uso, memoria
#   - RAM: uso porcentual, swap
#   - Disco: uso en particiones críticas
#   - Procesos: servicios clave de ORQUOR
#
# Alertas vía:
#   - Email (Resend API, usa RESEND_API_KEY del .env)
#   - Signal CLI (opcional, usa SIGNAL_CLI_PHONE)
#   - Log local (.monitor_alerts.log)
#
# Modos:
#   --once             Una sola ejecución, reporta estado y sale
#   --watch <secs>     Ejecuta en loop cada N segundos (default: 60)
#   --alert-test       Envía una alerta de prueba y sale
#   --json             Salida en formato JSON (para CI/integraciones)

set -euo pipefail

# ─── Colors ────────────────────────────────────────────────────────
BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
CYAN="\033[36m"
RESET="\033[0m"

log_info()  { echo -e "${BLUE}[monitor]${RESET} $1"; }
log_ok()    { echo -e "${GREEN}[monitor]${RESET} $1"; }
log_warn()  { echo -e "${YELLOW}[monitor]${RESET} $1"; }
log_error() { echo -e "${RED}[monitor]${RESET} $1"; }

# ─── Paths ─────────────────────────────────────────────────────────
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ALERT_LOG="${PROJECT_ROOT}/.monitor_alerts.log"
MONITOR_LOCK="${PROJECT_ROOT}/.monitor.lock"

# ─── Thresholds (configurable via env) ─────────────────────────────
GPU_TEMP_CRIT="${GPU_TEMP_CRIT:-85}"          # °C
GPU_MEM_CRIT="${GPU_MEM_CRIT:-95}"            # %
GPU_LOAD_CRIT="${GPU_LOAD_CRIT:-95}"          # %
RAM_CRIT="${RAM_CRIT:-90}"                    # %
DISK_CRIT="${DISK_CRIT:-90}"                  # %
SWAP_CRIT="${SWAP_CRIT:-50}"                  # %

# ─── Alert config ──────────────────────────────────────────────────
ALERT_EMAIL="${ALERT_EMAIL:-${EMAIL_TO_FOUNDER:-}}"   # from .env
RESEND_API_KEY="${RESEND_API_KEY:-}"
SIGNAL_CLI_PHONE="${SIGNAL_CLI_PHONE:-}"
ALERT_COOLDOWN="${ALERT_COOLDOWN:-300}"               # segundos entre alertas del mismo tipo
COOLDOWN_FILE="${PROJECT_ROOT}/.monitor_cooldowns"

# ─── Parse args ────────────────────────────────────────────────────
MODE="once"
WATCH_SECS=60
JSON_OUT="false"

for arg in "$@"; do
    case "$arg" in
        --once)         MODE="once" ;;
        --watch)
            MODE="watch"
            if [[ "${2:-}" =~ ^[0-9]+$ ]]; then
                WATCH_SECS="$2"
                shift 2 2>/dev/null || true
            fi
            ;;
        --alert-test)   MODE="alert-test" ;;
        --json)         JSON_OUT="true" ;;
        --help|-h)
            echo "Uso: $0 [--once|--watch <secs>|--alert-test|--json]"
            echo ""
            echo "  --once           Una sola ejecución y sale (default)"
            echo "  --watch <secs>   Monitoreo continuo cada N segundos"
            echo "  --alert-test     Enviar alerta de prueba"
            echo "  --json           Salida en formato JSON"
            echo ""
            echo "Thresholds configurables vía env:"
            echo "  GPU_TEMP_CRIT   (default: 85°C)"
            echo "  GPU_MEM_CRIT    (default: 95%)"
            echo "  RAM_CRIT        (default: 90%)"
            echo "  DISK_CRIT       (default: 90%)"
            exit 0
            ;;
    esac
done

# ─── Load .env ─────────────────────────────────────────────────────
if [ -f "${PROJECT_ROOT}/.env" ]; then
    set -a
    source "${PROJECT_ROOT}/.env"
    set +a
elif [ -f "${PROJECT_ROOT}/06-hermes/.env" ]; then
    set -a
    source "${PROJECT_ROOT}/06-hermes/.env"
    set +a
fi

# ─── Cooldown helper ───────────────────────────────────────────────
should_alert() {
    local alert_key="$1"
    local now
    now=$(date +%s)

    if [ ! -f "$COOLDOWN_FILE" ]; then
        touch "$COOLDOWN_FILE"
    fi

    local last_time
    last_time=$(grep "^${alert_key}=" "$COOLDOWN_FILE" 2>/dev/null | cut -d= -f2 || echo "0")

    if [ $((now - last_time)) -ge "$ALERT_COOLDOWN" ]; then
        # Update cooldown
        if grep -q "^${alert_key}=" "$COOLDOWN_FILE" 2>/dev/null; then
            sed -i "s/^${alert_key}=.*/${alert_key}=${now}/" "$COOLDOWN_FILE"
        else
            echo "${alert_key}=${now}" >> "$COOLDOWN_FILE"
        fi
        return 0
    fi
    return 1
}

# ─── Alert dispatcher ──────────────────────────────────────────────
send_alert() {
    local severity="$1"  # critical | warning
    local component="$2" # gpu | ram | disk
    local message="$3"

    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local alert_key="${severity}_${component}"

    # Cooldown check
    if ! should_alert "$alert_key"; then
        return 0
    fi

    # Log to file
    echo "[${timestamp}] ${severity^^} | ${component} | ${message}" >> "$ALERT_LOG"

    # Console
    if [ "$severity" = "critical" ]; then
        log_error "${component}: ${message}"
    else
        log_warn "${component}: ${message}"
    fi

    # Email via Resend API
    if [ -n "$RESEND_API_KEY" ] && [ -n "$ALERT_EMAIL" ]; then
        local subject="[ORQUOR] ${severity^^}: ${component}"
        curl -s -X POST https://api.resend.com/emails \
            -H "Authorization: Bearer ${RESEND_API_KEY}" \
            -H "Content-Type: application/json" \
            -d "{
                \"from\": \"hermes@orquor.com\",
                \"to\": \"${ALERT_EMAIL}\",
                \"subject\": \"${subject}\",
                \"text\": \"Timestamp: ${timestamp}\nComponent: ${component}\nSeverity: ${severity}\nMessage: ${message}\n\n— Orquor Monitor\"
            }" >/dev/null 2>&1 || true
    fi

    # Signal (optional)
    if [ -n "$SIGNAL_CLI_PHONE" ] && command -v signal-cli &>/dev/null; then
        signal-cli -a "+51999999999" send -m "[ORQUOR ${severity^^}] ${component}: ${message}" "$SIGNAL_CLI_PHONE" >/dev/null 2>&1 || true
    fi
}

# ─── GPU monitoring ────────────────────────────────────────────────
check_gpu() {
    if ! command -v nvidia-smi &>/dev/null; then
        [ "$JSON_OUT" != "true" ] && log_info "GPU: nvidia-smi no disponible (sin GPU NVIDIA detectada)"
        return 0
    fi

    local gpu_info
    gpu_info=$(nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw --format=csv,noheader,nounits 2>/dev/null || echo "")

    if [ -z "$gpu_info" ]; then
        [ "$JSON_OUT" != "true" ] && log_warn "GPU: no se pudo leer información de nvidia-smi"
        return 0
    fi

    while IFS=, read -r idx name temp util mem_used mem_total power; do
        # Trim whitespace
        idx=$(echo "$idx" | xargs)
        name=$(echo "$name" | xargs)
        temp=$(echo "$temp" | xargs)
        util=$(echo "$util" | xargs)
        mem_used=$(echo "$mem_used" | xargs)
        mem_total=$(echo "$mem_total" | xargs)
        power=$(echo "$power" | xargs)

        # Calculate memory percentage
        local mem_pct=0
        if [ -n "$mem_total" ] && [ "$mem_total" != "0" ] && [ -n "$mem_used" ]; then
            mem_pct=$(awk "BEGIN {printf \"%.1f\", ($mem_used/$mem_total)*100}")
        fi

        # Status determination
        local status="OK"
        [ -n "$temp" ] && [ "$(echo "$temp > $GPU_TEMP_CRIT" | bc -l 2>/dev/null || echo 0)" = "1" ] && status="CRIT"
        [ "$(echo "$util > $GPU_LOAD_CRIT" | bc -l 2>/dev/null || echo 0)" = "1" ] && [ "$status" != "CRIT" ] && status="WARN"
        [ "$(echo "$mem_pct > $GPU_MEM_CRIT" | bc -l 2>/dev/null || echo 0)" = "1" ] && status="CRIT"

        if [ "$JSON_OUT" = "true" ]; then
            echo "{\"type\":\"gpu\",\"index\":\"$idx\",\"name\":\"$name\",\"temp\":\"$temp\",\"util\":\"$util\",\"mem_used\":\"$mem_used\",\"mem_total\":\"$mem_total\",\"mem_pct\":\"$mem_pct\",\"power\":\"$power\",\"status\":\"$status\"}"
        else
            local icon="✓"
            [ "$status" = "WARN" ] && icon="${YELLOW}⚠${RESET}"
            [ "$status" = "CRIT" ] && icon="${RED}✗${RESET}"

            echo -e "  GPU ${idx} ${icon} | ${name} | ${temp}°C | ${util}% load | ${mem_used}/${mem_total} MiB (${mem_pct}%) | ${power}W"
        fi

        # Alerts
        if [ "$status" = "CRIT" ]; then
            send_alert "critical" "gpu" "GPU ${idx} (${name}): ${temp}°C / ${mem_pct}% mem / ${util}% load"
        elif [ "$status" = "WARN" ]; then
            send_alert "warning" "gpu" "GPU ${idx} (${name}): ${util}% load elevado"
        fi
    done <<< "$gpu_info"
}

# ─── RAM monitoring ────────────────────────────────────────────────
check_ram() {
    local mem_info
    mem_info=$(free -m 2>/dev/null | awk '/^Mem:/ {printf "%d %d %d %d", $2, $3, $4, $7}' || echo "")
    local swap_info
    swap_info=$(free -m 2>/dev/null | awk '/^Swap:/ {printf "%d %d %d", $2, $3, $4}' || echo "")

    if [ -z "$mem_info" ]; then
        [ "$JSON_OUT" != "true" ] && log_warn "RAM: no se pudo leer información"
        return 0
    fi

    read -r total used free available <<< "$mem_info"
    local pct_used=0
    [ -n "$total" ] && [ "$total" != "0" ] && pct_used=$(awk "BEGIN {printf \"%.1f\", ($used/$total)*100}")

    local status="OK"
    [ "$(echo "$pct_used > $RAM_CRIT" | bc -l 2>/dev/null || echo 0)" = "1" ] && status="CRIT"

    # Swap check
    local swap_pct=0
    local swap_status="OK"
    if [ -n "$swap_info" ]; then
        read -r sw_total sw_used sw_free <<< "$swap_info"
        [ -n "$sw_total" ] && [ "$sw_total" != "0" ] && swap_pct=$(awk "BEGIN {printf \"%.1f\", ($sw_used/$sw_total)*100}")
        [ "$(echo "$swap_pct > $SWAP_CRIT" | bc -l 2>/dev/null || echo 0)" = "1" ] && swap_status="WARN"
    fi

    if [ "$JSON_OUT" = "true" ]; then
        echo "{\"type\":\"ram\",\"total_mb\":\"$total\",\"used_mb\":\"$used\",\"free_mb\":\"$free\",\"available_mb\":\"$available\",\"pct_used\":\"$pct_used\",\"swap_total_mb\":\"${sw_total:-0}\",\"swap_used_mb\":\"${sw_used:-0}\",\"swap_pct\":\"$swap_pct\",\"status\":\"$status\"}"
    else
        local icon="✓"
        [ "$status" = "CRIT" ] && icon="${RED}✗${RESET}"

        echo -e "  RAM  ${icon} | ${used}/${total} MB (${pct_used}%) | available: ${available} MB"
        if [ "$swap_pct" != "0" ]; then
            local sw_icon="✓"
            [ "$swap_status" = "WARN" ] && sw_icon="${YELLOW}⚠${RESET}"
            echo -e "  SWAP ${sw_icon} | ${sw_used:-0}/${sw_total:-0} MB (${swap_pct}%)"
        fi
    fi

    if [ "$status" = "CRIT" ]; then
        send_alert "critical" "ram" "RAM usage: ${pct_used}% (${used}/${total} MB)"
    fi

    if [ "$swap_status" = "WARN" ]; then
        send_alert "warning" "ram" "Swap usage: ${swap_pct}%"
    fi
}

# ─── Disk monitoring ───────────────────────────────────────────────
check_disk() {
    # Check project partition and common mount points
    local partitions
    partitions=$(df -h "$PROJECT_ROOT" / /home /var 2>/dev/null | tail -n +2 || echo "")

    if [ -z "$partitions" ]; then
        [ "$JSON_OUT" != "true" ] && log_warn "Disk: no se pudo leer información"
        return 0
    fi

    # deduplicate by mount point
    echo "$partitions" | sort -u -k6 | while read -r fs size used avail pct mnt; do
        pct_num=$(echo "$pct" | tr -d '%')

        local status="OK"
        [ "$pct_num" -ge "$DISK_CRIT" ] && status="CRIT"
        [ "$pct_num" -ge $((DISK_CRIT - 10)) ] && [ "$status" != "CRIT" ] && status="WARN"

        if [ "$JSON_OUT" = "true" ]; then
            echo "{\"type\":\"disk\",\"filesystem\":\"$fs\",\"size\":\"$size\",\"used\":\"$used\",\"avail\":\"$avail\",\"pct\":\"$pct\",\"mount\":\"$mnt\",\"status\":\"$status\"}"
        else
            local icon="✓"
            [ "$status" = "WARN" ] && icon="${YELLOW}⚠${RESET}"
            [ "$status" = "CRIT" ] && icon="${RED}✗${RESET}"

            echo -e "  DISK ${icon} | ${mnt} | ${used}/${size} (${pct}) | free: ${avail}"
        fi

        if [ "$status" = "CRIT" ]; then
            send_alert "critical" "disk" "Disk ${mnt}: ${pct} full (${used}/${size})"
        elif [ "$status" = "WARN" ]; then
            send_alert "warning" "disk" "Disk ${mnt}: ${pct} full — approaching limit"
        fi
    done
}

# ─── Process monitoring ────────────────────────────────────────────
check_processes() {
    local services=("python" "postgres" "qdrant" "nginx" "docker")
    [ "$JSON_OUT" != "true" ] && echo ""

    for svc in "${services[@]}"; do
        local pids
        pids=$(pgrep -f "$svc" 2>/dev/null || echo "")
        local count
        count=$(echo "$pids" | grep -c . || echo "0")

        if [ "$count" -gt 0 ]; then
            if [ "$JSON_OUT" = "true" ]; then
                echo "{\"type\":\"process\",\"service\":\"$svc\",\"count\":\"$count\",\"status\":\"running\"}"
            else
                echo -e "  ${GREEN}✓${RESET} ${svc}: ${count} proceso(s)"
            fi
        else
            if [ "$JSON_OUT" = "true" ]; then
                echo "{\"type\":\"process\",\"service\":\"$svc\",\"count\":\"0\",\"status\":\"down\"}"
            else
                echo -e "  ${BLUE}○${RESET} ${svc}: no detectado"
            fi
        fi
    done
}

# ─── Alert test ────────────────────────────────────────────────────
alert_test() {
    echo -e "${BOLD}=== ORQUOR Monitor — Alert Test ===${RESET}"
    echo ""
    log_info "Enviando alerta de prueba..."

    send_alert "critical" "test" "Alerta de prueba desde monitor.sh — $(date)"

    echo ""
    log_ok "Alerta enviada. Verificar:"
    [ -n "$ALERT_EMAIL" ] && echo "  Email: ${ALERT_EMAIL}"
    [ -n "$SIGNAL_CLI_PHONE" ] && echo "  Signal: ${SIGNAL_CLI_PHONE}"
    echo "  Log:   ${ALERT_LOG}"
}

# ─── Single run ────────────────────────────────────────────────────
run_once() {
    echo -e "${BOLD}=== ORQUOR System Monitor ===${RESET}"
    echo -e "  $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo ""

    echo -e "${BOLD}── GPU ──${RESET}"
    check_gpu

    echo ""
    echo -e "${BOLD}── RAM ──${RESET}"
    check_ram

    echo ""
    echo -e "${BOLD}── Disk ──${RESET}"
    check_disk

    echo ""
    echo -e "${BOLD}── Processes ──${RESET}"
    check_processes

    echo ""
    echo -e "${BOLD}=== Monitor Complete ===${RESET}"
}

# ─── Main ──────────────────────────────────────────────────────────
main() {
    case "$MODE" in
        once)
            run_once
            ;;
        watch)
            echo -e "${BOLD}=== ORQUOR Monitor — Watching every ${WATCH_SECS}s ===${RESET}"
            echo -e "  Log: ${ALERT_LOG}"
            echo -e "  Ctrl+C para detener"
            echo ""

            # Trap for clean exit
            trap 'echo ""; log_info "Monitor detenido."; rm -f "$MONITOR_LOCK"; exit 0' INT TERM

            echo $$ > "$MONITOR_LOCK"

            while true; do
                echo -e "\n${CYAN}── $(date '+%H:%M:%S') ──${RESET}"
                check_gpu | head -4
                check_ram | head -2
                check_disk | head -4
                sleep "$WATCH_SECS"
            done
            ;;
        alert-test)
            alert_test
            ;;
    esac
}

main
