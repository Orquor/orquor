#!/bin/bash
# health-check.sh — Verificación de estado del proyecto ORQUOR
# Uso: ./scripts/health-check.sh [--quick|--full|--ci]
#
# Modos:
#   --quick   Solo estructura de archivos + git status (rápido)
#   --full    Quick + tests + connectivity + env (completo, default)
#   --ci      Salida mínima para CI/CD, código de salida 0/1
#
# Chequea:
#   1. Integridad de archivos (directorios core existen, no vacíos)
#   2. Git (rama, commits, remoto, estado limpio)
#   3. Tests (pytest en 06-hermes si existe)
#   4. Variables de entorno requeridas (.env presente)
#   5. Conectividad (Hostinger FTP, orquor.com HTTP)

set -euo pipefail

# ─── Colors ────────────────────────────────────────────────────────
BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
RESET="\033[0m"

PASS=0
WARN=0
FAIL=0
CI_MODE="false"

pass() { PASS=$((PASS + 1)); [ "$CI_MODE" != "true" ] && echo -e "  ${GREEN}✓${RESET} $1"; }
warn() { WARN=$((WARN + 1)); [ "$CI_MODE" != "true" ] && echo -e "  ${YELLOW}⚠${RESET} $1"; }
fail() { FAIL=$((FAIL + 1)); [ "$CI_MODE" != "true" ] && echo -e "  ${RED}✗${RESET} $1"; }
info() { [ "$CI_MODE" != "true" ] && echo -e "${BLUE}[health]${RESET} $1"; }
section() { [ "$CI_MODE" != "true" ] && echo -e "\n${BOLD}── $1 ──${RESET}"; }

# ─── Parse args ────────────────────────────────────────────────────
MODE="full"
for arg in "$@"; do
    case "$arg" in
        --quick) MODE="quick" ;;
        --full)  MODE="full" ;;
        --ci)    MODE="ci"; CI_MODE="true" ;;
        --help|-h)
            echo "Uso: $0 [--quick|--full|--ci]"
            echo "  --quick  Sólo archivos + git"
            echo "  --full   Completo: archivos, git, tests, env, connectivity (default)"
            echo "  --ci     Salida mínima, exit code 0 si todo OK"
            exit 0
            ;;
    esac
done

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

[ "$CI_MODE" != "true" ] && echo -e "${BOLD}=== ORQUOR Health Check${RESET} ===\n"

# ─── 1. File structure ─────────────────────────────────────────────
section "1. Estructura de archivos"

REQUIRED_DIRS=(
    "01-action-board"
    "02-brand"
    "03-whitepaper-acto"
    "04-web"
    "05-pitch-deck"
    "06-hermes"
    "07-legal"
    "08-prospects"
    "09-content-calendar"
    "10-migration-runbook"
    "scripts"
    ".github/workflows"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    full_dir="${PROJECT_ROOT}/${dir}"
    if [ -d "$full_dir" ]; then
        # Check directory is not empty (exclude .gitkeep)
        file_count=$(find "$full_dir" -type f -not -name '.gitkeep' 2>/dev/null | wc -l)
        if [ "$file_count" -gt 0 ]; then
            pass "directorio: ${dir} (${file_count} archivos)"
        else
            warn "directorio: ${dir} (vacío)"
        fi
    else
        fail "directorio: ${dir} (NO EXISTE)"
    fi
done

# Check critical files
CRITICAL_FILES=(
    "README.md"
    "LICENSE"
    "CONTRIBUTING.md"
    ".gitignore"
    "04-web/index.html"
    "04-web/demo.html"
    "04-web/404.html"
    "06-hermes/requirements.txt"
    ".github/workflows/ci.yml"
)

for f in "${CRITICAL_FILES[@]}"; do
    full_f="${PROJECT_ROOT}/${f}"
    if [ -f "$full_f" ]; then
        if [ -s "$full_f" ]; then
            pass "archivo: ${f}"
        else
            warn "archivo: ${f} (vacío)"
        fi
    else
        fail "archivo: ${f} (NO EXISTE)"
    fi
done

# Check 04-web landing files
LANDING_FILES=$(find "${PROJECT_ROOT}/04-web" -type f -not -path '*/\.*' 2>/dev/null | wc -l)
if [ "$LANDING_FILES" -ge 3 ]; then
    pass "landing: ${LANDING_FILES} archivos en 04-web/"
else
    warn "landing: solo ${LANDING_FILES} archivos en 04-web/"
fi

# ─── 2. Git status ─────────────────────────────────────────────────
section "2. Git"

cd "$PROJECT_ROOT"

if git rev-parse --git-dir > /dev/null 2>&1; then
    pass "git repo detectado"

    BRANCH=$(git branch --show-current 2>/dev/null || echo "?")
    if [ -n "$BRANCH" ] && [ "$BRANCH" != "?" ]; then
        pass "rama: ${BRANCH}"
    else
        warn "rama: detached HEAD o sin rama"
    fi

    REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
    if [ -n "$REMOTE" ]; then
        pass "remoto: ${REMOTE}"
    else
        warn "remoto: no configurado"
    fi

    # Check if up to date with remote (no network required — compares local refs)
    LOCAL=$(git rev-parse @ 2>/dev/null || echo "")
    REMOTE_REF=$(git rev-parse @{u} 2>/dev/null || echo "")
    if [ -z "$REMOTE_REF" ]; then
        info "  (sin upstream branch configurado)"
    elif [ "$LOCAL" = "$REMOTE_REF" ]; then
        pass "sincronizado con remoto"
    elif [ -n "$LOCAL" ]; then
        BASE=$(git merge-base @ @{u} 2>/dev/null || echo "")
        if [ "$LOCAL" = "$BASE" ]; then
            warn "atrás del remoto — necesita pull"
        elif [ "$REMOTE_REF" = "$BASE" ]; then
            warn "adelante del remoto — necesita push"
        else
            warn "divergido del remoto"
        fi
    fi

    # Working tree clean?
    if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
        pass "working tree limpio"
    else
        CHANGED=$(git status --porcelain 2>/dev/null | wc -l)
        warn "working tree sucio (${CHANGED} cambios)"
    fi

    # Last commit
    LAST_COMMIT=$(git log -1 --format="%h — %s (%ar)" 2>/dev/null || echo "?")
    info "  último commit: ${LAST_COMMIT}"
else
    fail "no es un repositorio git"
fi

# ─── 3. Tests (full mode only) ─────────────────────────────────────
if [ "$MODE" != "quick" ]; then
    section "3. Tests (06-hermes)"

    if [ -d "${PROJECT_ROOT}/06-hermes/verifiers" ]; then
        TEST_FILES=$(find "${PROJECT_ROOT}/06-hermes/verifiers" -name '*.py' | wc -l)
        info "  verifiers encontrados: ${TEST_FILES}"

        if command -v python3 &>/dev/null; then
            # Try pytest (might be in venv)
            PYTEST=""
            if [ -f "${PROJECT_ROOT}/06-hermes/.venv/bin/pytest" ]; then
                PYTEST="${PROJECT_ROOT}/06-hermes/.venv/bin/pytest"
            elif command -v pytest &>/dev/null; then
                PYTEST="pytest"
            fi

            if [ -n "$PYTEST" ]; then
                cd "${PROJECT_ROOT}/06-hermes"
                # Run pytest with verbose output, capture result
                TEST_OUTPUT=$($PYTEST verifiers/ -v --tb=short 2>&1) && TEST_EXIT=$? || TEST_EXIT=$?
                cd "$PROJECT_ROOT"

                PASSED=$(echo "$TEST_OUTPUT" | grep -c "PASSED" || true)
                FAILED_TESTS=$(echo "$TEST_OUTPUT" | grep -c "FAILED" || true)
                TOTAL_TESTS=$((PASSED + FAILED_TESTS))

                if [ "$TEST_EXIT" -eq 0 ]; then
                    pass "tests: ${TOTAL_TESTS}/${TOTAL_TESTS} passed"
                else
                    fail "tests: ${FAILED_TESTS}/${TOTAL_TESTS} fallaron"
                fi
            else
                warn "pytest no encontrado (instalar: pip install pytest)"
            fi
        else
            warn "python3 no encontrado"
        fi
    else
        warn "directorio verifiers/ no encontrado en 06-hermes/"
    fi
fi

# ─── 4. Environment (full mode only) ───────────────────────────────
if [ "$MODE" != "quick" ]; then
    section "4. Variables de entorno y .env"

    # Check .env file
    if [ -f "${PROJECT_ROOT}/.env" ]; then
        pass ".env presente"
    elif [ -f "${PROJECT_ROOT}/06-hermes/.env" ]; then
        pass ".env presente en 06-hermes/"
    else
        warn ".env no encontrado — copia .env.example si existe"
    fi

    # Check .env.example exists
    if [ -f "${PROJECT_ROOT}/.env.example" ]; then
        pass ".env.example presente"
    else
        warn ".env.example no encontrado en raíz"
    fi

    # Load .env if it exists
    if [ -f "${PROJECT_ROOT}/.env" ]; then
        set -a
        source "${PROJECT_ROOT}/.env"
        set +a
    elif [ -f "${PROJECT_ROOT}/06-hermes/.env" ]; then
        set -a
        source "${PROJECT_ROOT}/06-hermes/.env"
        set +a
    fi

    # Check critical env vars
    REQUIRED_VARS=(
        "HOSTINGER_FTP_USER"
        "HOSTINGER_FTP_PASS"
    )
    OPTIONAL_VARS=(
        "ANTHROPIC_API_KEY"
        "OPENAI_API_KEY"
        "DATABASE_URL"
        "QDRANT_URL"
        "RESEND_API_KEY"
        "LANGSMITH_API_KEY"
        "GITHUB_TOKEN"
        "HERMES_MODE"
    )

    for var in "${REQUIRED_VARS[@]}"; do
        if [ -n "${!var:-}" ]; then
            pass "env: ${var} definida"
        else
            fail "env: ${var} NO definida"
        fi
    done

    for var in "${OPTIONAL_VARS[@]}"; do
        if [ -n "${!var:-}" ]; then
            pass "env: ${var} definida"
        else
            info "  env: ${var} (no definida, opcional)"
        fi
    done
fi

# ─── 5. Connectivity (full mode only) ──────────────────────────────
if [ "$MODE" != "quick" ]; then
    section "5. Conectividad"

    # Check orquor.com HTTP
    if command -v curl &>/dev/null; then
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://orquor.com 2>/dev/null || echo "000")
        case "$HTTP_CODE" in
            200|301|302) pass "orquor.com: HTTP ${HTTP_CODE}" ;;
            *)           warn "orquor.com: HTTP ${HTTP_CODE}" ;;
        esac
    else
        info "  curl no disponible, omitiendo check HTTP"
    fi

    # Check Hostinger FTP reachable
    HOSTINGER_FTP_HOST="${HOSTINGER_FTP_HOST:-ftp.orquor.com}"
    if command -v nc &>/dev/null; then
        if echo | nc -w 5 "${HOSTINGER_FTP_HOST}" 21 >/dev/null 2>&1; then
            pass "FTP: ${HOSTINGER_FTP_HOST}:21 reachable"
        else
            warn "FTP: ${HOSTINGER_FTP_HOST}:21 no accesible (quizás bloqueado)"
        fi
    else
        info "  nc no disponible, omitiendo check FTP"
    fi

    # Check lftp available for deployments
    if command -v lftp &>/dev/null; then
        pass "lftp disponible (FTP deploy)"
    else
        warn "lftp no instalado (necesario para deploy FTP)"
    fi
fi

# ─── Summary ───────────────────────────────────────────────────────
section "Resumen"

TOTAL=$((PASS + WARN + FAIL))

[ "$CI_MODE" != "true" ] && echo ""
pass "${PASS} checks pasaron"
[ "$WARN" -gt 0 ] && warn "${WARN} advertencias"
[ "$FAIL" -gt 0 ] && fail "${FAIL} fallos"

if [ "$FAIL" -eq 0 ] && [ "$WARN" -eq 0 ]; then
    [ "$CI_MODE" != "true" ] && echo -e "\n${GREEN}${BOLD}✓ PROYECTO SALUDABLE${RESET}"
elif [ "$FAIL" -eq 0 ]; then
    [ "$CI_MODE" != "true" ] && echo -e "\n${YELLOW}${BOLD}△ Proyecto OK con advertencias${RESET}"
else
    [ "$CI_MODE" != "true" ] && echo -e "\n${RED}${BOLD}✗ PROBLEMAS DETECTADOS — Revisar antes de deploy${RESET}"
fi

exit "$FAIL"
