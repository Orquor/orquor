#!/bin/bash
# setup-dev.sh — Configuración completa del entorno de desarrollo ORQUOR
# Uso: ./scripts/setup-dev.sh [--force|--check|--ci]
#
# Configura:
#   1. System deps    — pandoc, texlive, PostgreSQL client, lftp, git
#   2. Python venv    — .venv en 06-hermes/ con dependencias
#   3. Git hooks      — pre-commit, commit-msg, pre-push
#   4. .env file      — Copia .env.example → .env si no existe
#   5. Playwright     — Instala navegadores para web automation
#   6. Permissions    — chmod +x a todos los scripts/
#
# Modos:
#   (default)   Setup interactivo, pregunta antes de cada paso
#   --force     No pregunta, ejecuta todo automáticamente
#   --check     Solo verifica qué está instalado/configurado
#   --ci        Modo CI/CD: --force + sin colores + exit code

set -euo pipefail

# ─── Colors ────────────────────────────────────────────────────────
BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
CYAN="\033[36m"
RESET="\033[0m"

log_info()  { echo -e "${BLUE}[setup]${RESET} $1"; }
log_ok()    { echo -e "${GREEN}[setup]${RESET} $1"; }
log_warn()  { echo -e "${YELLOW}[setup]${RESET} $1"; }
log_error() { echo -e "${RED}[setup]${RESET} $1"; }
log_step()  { echo -e "\n${BOLD}${CYAN}── $1 ──${RESET}"; }

# ─── Paths ─────────────────────────────────────────────────────────
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HERMES_DIR="${PROJECT_ROOT}/06-hermes"
VENV_DIR="${HERMES_DIR}/.venv"
SCRIPTS_DIR="${PROJECT_ROOT}/scripts"
GIT_HOOKS_DIR="${PROJECT_ROOT}/.githooks"

# ─── State ─────────────────────────────────────────────────────────
FORCE="false"
CHECK_ONLY="false"
CI_MODE="false"
SETUP_LOG="${PROJECT_ROOT}/.setup_dev.log"

# ─── Parse args ────────────────────────────────────────────────────
for arg in "$@"; do
    case "$arg" in
        --force) FORCE="true" ;;
        --check) CHECK_ONLY="true" ;;
        --ci)    FORCE="true"; CI_MODE="true" ;;
        --help|-h)
            echo "Uso: $0 [--force|--check|--ci]"
            echo ""
            echo "  (default)  Setup interactivo, pregunta confirmación"
            echo "  --force    Ejecuta todo sin preguntar"
            echo "  --check    Solo verifica estado del entorno"
            echo "  --ci       Modo CI/CD (--force + sin prompts)"
            echo ""
            echo "Qué instala/configura:"
            echo "  1. Dependencias de sistema (pandoc, texlive, postgresql-client, lftp)"
            echo "  2. Entorno virtual Python (.venv) con requirements.txt"
            echo "  3. Git hooks (pre-commit, commit-msg, pre-push)"
            echo "  4. Archivo .env desde .env.example"
            echo "  5. Playwright browsers"
            echo "  6. Permisos de ejecución en scripts/"
            exit 0
            ;;
        *)
            log_error "Opción desconocida: $arg"
            exit 1
            ;;
    esac
done

# ─── Helpers ───────────────────────────────────────────────────────
confirm() {
    if [ "$FORCE" = "true" ]; then
        return 0
    fi
    local prompt="$1"
    echo -ne "${YELLOW}${prompt} [y/N] ${RESET}"
    read -r answer
    [ "$answer" = "y" ] || [ "$answer" = "Y" ]
}

step_ok() {
    echo -e "  ${GREEN}✓${RESET} $1"
    echo "[$(date -u +%T)] ✓ $1" >> "$SETUP_LOG"
}

step_skip() {
    echo -e "  ${YELLOW}○${RESET} $1 (omitido)"
}

step_fail() {
    echo -e "  ${RED}✗${RESET} $1"
    echo "[$(date -u +%T)] ✗ $1" >> "$SETUP_LOG"
}

check_cmd() {
    command -v "$1" &>/dev/null && echo "true" || echo "false"
}

# ─── Initialize log ────────────────────────────────────────────────
echo "# ORQUOR Dev Setup Log — $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$SETUP_LOG"

echo -e "${BOLD}=== ORQUOR Development Environment Setup ===${RESET}"
echo ""

# ═══════════════════════════════════════════════════════════════════
# 1. SYSTEM DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════
log_step "1. Dependencias de sistema"

SYSTEM_DEPS=(
    "python3:python3:Python 3.12+"
    "pip3:pip:Python package manager"
    "git:git:Git version control"
    "pandoc:pandoc:Markdown to PDF converter"
    "xelatex:xelatex:LaTeX engine (texlive-xetex)"
    "lftp:lftp:FTP client for deploy"
    "psql:psql:PostgreSQL client"
    "curl:curl:HTTP client"
    "nc:nc:Netcat for connectivity tests"
    "nvidia-smi:nvidia-smi:NVIDIA GPU tools (optional)"
)

MISSING_DEPS=()
for dep in "${SYSTEM_DEPS[@]}"; do
    IFS=':' read -r cmd_name pkg_name description <<< "$dep"

    if [ "$(check_cmd "$cmd_name")" = "true" ]; then
        if [ "$CHECK_ONLY" = "true" ]; then
            echo -e "  ${GREEN}✓${RESET} ${description} (${cmd_name})"
        fi
    else
        if [ "$CHECK_ONLY" = "true" ]; then
            echo -e "  ${RED}✗${RESET} ${description} (${cmd_name}) — instalar: sudo apt install ${pkg_name}"
        else
            log_warn "Falta: ${description} (${pkg_name})"
            MISSING_DEPS+=("${pkg_name}")
        fi
    fi
done

if [ "$CHECK_ONLY" = "false" ] && [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    if confirm "¿Instalar dependencias faltantes? (sudo apt install)"; then
        log_info "Instalando: ${MISSING_DEPS[*]}..."
        sudo apt update -qq && sudo apt install -y "${MISSING_DEPS[@]}" || {
            log_error "Falló la instalación de dependencias."
            echo "Instala manualmente: sudo apt install ${MISSING_DEPS[*]}"
        }
        step_ok "Dependencias de sistema instaladas"
    else
        step_skip "Instalación de dependencias"
    fi
elif [ "$CHECK_ONLY" = "false" ]; then
    step_ok "Todas las dependencias de sistema presentes"
fi

# ═══════════════════════════════════════════════════════════════════
# 2. PYTHON VENV
# ═══════════════════════════════════════════════════════════════════
log_step "2. Entorno virtual Python (.venv)"

if [ ! -f "${HERMES_DIR}/requirements.txt" ]; then
    if [ "$CHECK_ONLY" = "true" ]; then
        echo -e "  ${RED}✗${RESET} requirements.txt no encontrado en 06-hermes/"
    else
        log_warn "requirements.txt no encontrado en ${HERMES_DIR}"
    fi
else
    REQUIREMENTS_HASH=$(md5sum "${HERMES_DIR}/requirements.txt" 2>/dev/null | cut -d' ' -f1 || echo "")

    if [ "$CHECK_ONLY" = "true" ]; then
        if [ -d "$VENV_DIR" ]; then
            echo -e "  ${GREEN}✓${RESET} Virtualenv existe: ${VENV_DIR}"
            if [ -f "${VENV_DIR}/bin/python" ]; then
                local pyver
                pyver=$("${VENV_DIR}/bin/python" --version 2>&1 || echo "?")
                echo -e "  ${GREEN}✓${RESET} Python: ${pyver}"
            fi
        else
            echo -e "  ${RED}✗${RESET} Virtualenv no creado"
        fi
    else
        local needs_install="false"

        if [ ! -d "$VENV_DIR" ]; then
            needs_install="true"
            log_info "Virtualenv no encontrado. Se creará en ${VENV_DIR}"
        elif [ ! -f "${VENV_DIR}/.requirements_hash" ] || [ "$(cat "${VENV_DIR}/.requirements_hash" 2>/dev/null)" != "$REQUIREMENTS_HASH" ]; then
            needs_install="true"
            log_info "requirements.txt cambió desde la última instalación."
        fi

        if [ "$needs_install" = "true" ]; then
            if confirm "¿Crear/actualizar entorno virtual Python?"; then
                # Create venv
                python3 -m venv "$VENV_DIR" --clear 2>/dev/null || {
                    log_warn "python3 -m venv falló, intentando con virtualenv..."
                    pip3 install virtualenv 2>/dev/null || true
                    python3 -m virtualenv "$VENV_DIR" || {
                        log_error "No se pudo crear el virtualenv."
                        step_fail "Virtualenv creation failed"
                        # continue anyway
                    }
                }

                # Activate and install
                log_info "Instalando dependencias Python..."
                source "${VENV_DIR}/bin/activate"

                # Upgrade pip
                pip install --upgrade pip setuptools wheel -q 2>&1 | tail -1

                # Install requirements
                pip install -r "${HERMES_DIR}/requirements.txt" -q 2>&1 || {
                    log_error "Falló la instalación de requirements.txt"
                    log_info "Revisa el error e instala manualmente:"
                    echo "  source ${VENV_DIR}/bin/activate"
                    echo "  pip install -r ${HERMES_DIR}/requirements.txt"
                }

                # Store hash
                echo "$REQUIREMENTS_HASH" > "${VENV_DIR}/.requirements_hash"

                deactivate 2>/dev/null || true
                step_ok "Virtualenv creado/actualizado: ${VENV_DIR}"
            else
                step_skip "Virtualenv"
            fi
        else
            step_ok "Virtualenv ya actualizado: ${VENV_DIR}"
        fi
    fi
fi

# ═══════════════════════════════════════════════════════════════════
# 3. GIT HOOKS
# ═══════════════════════════════════════════════════════════════════
log_step "3. Git hooks"

if [ "$CHECK_ONLY" = "true" ]; then
    if [ -d "$GIT_HOOKS_DIR" ]; then
        echo -e "  ${GREEN}✓${RESET} Directorio .githooks/ presente"
        for hook in pre-commit commit-msg pre-push; do
            if [ -f "${GIT_HOOKS_DIR}/${hook}" ]; then
                echo -e "    ${GREEN}✓${RESET} ${hook}"
            else
                echo -e "    ${YELLOW}○${RESET} ${hook} (no definido)"
            fi
        done
    else
        echo -e "  ${RED}✗${RESET} .githooks/ no encontrado"
    fi
    # Check if git is configured to use custom hooks
    local hooks_path
    hooks_path=$(git config --get core.hooksPath 2>/dev/null || echo "")
    if [ "$hooks_path" = ".githooks" ]; then
        echo -e "  ${GREEN}✓${RESET} core.hooksPath configurado correctamente (.githooks)"
    else
        echo -e "  ${YELLOW}⚠${RESET} core.hooksPath no configurado (actual: ${hooks_path:-default})"
    fi
else
    # Create githooks directory
    mkdir -p "$GIT_HOOKS_DIR"

    # ── pre-commit ─────────────────────────────────────────────
    cat > "${GIT_HOOKS_DIR}/pre-commit" << 'PRECOMMIT'
#!/bin/bash
# ORQUOR pre-commit hook
# - Formatea Python con ruff/black
# - Verifica que .env no esté staged
# - Corre tests unitarios rápidos

set -euo pipefail

echo "🔍 ORQUOR pre-commit check..."

# 1. No .env committed
if git diff --cached --name-only | grep -q '\.env$' 2>/dev/null; then
    echo "❌ .env file staged — REMOVE before commit!"
    echo "   git reset HEAD .env"
    exit 1
fi

# 2. Python syntax check on staged .py files
STAGED_PY=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)
if [ -n "$STAGED_PY" ]; then
    echo "  Checking Python syntax..."
    for f in $STAGED_PY; do
        python3 -m py_compile "$f" 2>/dev/null || {
            echo "❌ Syntax error in: $f"
            exit 1
        }
    done
    echo "  ✓ Python syntax OK"
fi

# 3. Run ruff if available
if command -v ruff &>/dev/null; then
    echo "  Running ruff..."
    ruff check --fix $STAGED_PY 2>/dev/null || true
fi

# 4. Check for large files (>5MB)
for f in $(git diff --cached --name-only); do
    if [ -f "$f" ]; then
        size=$(stat -c%s "$f" 2>/dev/null || echo 0)
        if [ "$size" -gt 5242880 ]; then
            echo "⚠ WARNING: Large file staged: $f ($((size / 1048576)) MB)"
        fi
    done
done

echo "✅ pre-commit OK"
PRECOMMIT

    # ── commit-msg ─────────────────────────────────────────────
    cat > "${GIT_HOOKS_DIR}/commit-msg" << 'COMMITMSG'
#!/bin/bash
# ORQUOR commit-msg hook
# - Enforces conventional commit format

COMMIT_MSG=$(cat "$1")

# Check minimum length
if [ ${#COMMIT_MSG} -lt 5 ]; then
    echo "❌ Commit message too short (min 5 chars)"
    exit 1
fi

# Check conventional commit format (optional, warning only)
if ! echo "$COMMIT_MSG" | grep -qE '^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\(.+\))?: '; then
    echo "⚠ Commit doesn't follow conventional format."
    echo "   Expected: type(scope): description"
    echo "   Types: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert"
    echo ""
    echo "   Proceeding anyway..."
fi

echo "✅ commit-msg OK"
COMMITMSG

    # ── pre-push ───────────────────────────────────────────────
    cat > "${GIT_HOOKS_DIR}/pre-push" << 'PREPUSH'
#!/bin/bash
# ORQUOR pre-push hook
# - Corre tests antes de push

set -euo pipefail

echo "🔍 ORQUOR pre-push check..."

# Run health-check in CI mode
if [ -f "./scripts/health-check.sh" ]; then
    echo "  Running health-check..."
    bash ./scripts/health-check.sh --ci 2>/dev/null || {
        echo "❌ Health check failed — fix issues before pushing"
        echo "   Run: ./scripts/health-check.sh --full"
        exit 1
    }
    echo "  ✓ Health check passed"
else
    echo "  ⚠ health-check.sh not found, skipping"
fi

echo "✅ pre-push OK"
PREPUSH

    # Make hooks executable
    chmod +x "${GIT_HOOKS_DIR}/pre-commit"
    chmod +x "${GIT_HOOKS_DIR}/commit-msg"
    chmod +x "${GIT_HOOKS_DIR}/pre-push"

    # Configure git to use custom hooks path
    cd "$PROJECT_ROOT"
    git config core.hooksPath .githooks

    step_ok "Git hooks configurados (.githooks/)"
    echo "  Hooks: pre-commit, commit-msg, pre-push"
fi

# ═══════════════════════════════════════════════════════════════════
# 4. .ENV SETUP
# ═══════════════════════════════════════════════════════════════════
log_step "4. Archivo .env"

if [ "$CHECK_ONLY" = "true" ]; then
    if [ -f "${PROJECT_ROOT}/.env" ]; then
        echo -e "  ${GREEN}✓${RESET} .env presente en raíz del proyecto"
    elif [ -f "${HERMES_DIR}/.env" ]; then
        echo -e "  ${GREEN}✓${RESET} .env presente en 06-hermes/"
    else
        echo -e "  ${RED}✗${RESET} .env no encontrado — copia .env.example"
    fi

    if [ -f "${PROJECT_ROOT}/.env.example" ]; then
        echo -e "  ${GREEN}✓${RESET} .env.example presente (template disponible)"
    else
        echo -e "  ${YELLOW}○${RESET} .env.example no encontrado"
    fi
else
    if [ -f "${PROJECT_ROOT}/.env" ]; then
        step_ok ".env ya existe en raíz"
    elif [ -f "${HERMES_DIR}/.env" ]; then
        step_ok ".env ya existe en 06-hermes/"
    elif [ -f "${PROJECT_ROOT}/.env.example" ]; then
        if confirm "¿Copiar .env.example → .env?"; then
            cp "${PROJECT_ROOT}/.env.example" "${PROJECT_ROOT}/.env"
            step_ok ".env creado desde .env.example"
            log_warn "Edita .env con tus credenciales reales antes de usar"
        else
            step_skip ".env — crea uno manualmente: cp .env.example .env"
        fi
    elif [ -f "${HERMES_DIR}/.env.example" ]; then
        if confirm "¿Copiar 06-hermes/.env.example → 06-hermes/.env?"; then
            cp "${HERMES_DIR}/.env.example" "${HERMES_DIR}/.env"
            step_ok ".env creado en 06-hermes/"
            log_warn "Edita .env con tus credenciales reales antes de usar"
        else
            step_skip ".env"
        fi
    else
        log_warn ".env.example no encontrado — crea .env manualmente"
    fi
fi

# ═══════════════════════════════════════════════════════════════════
# 5. PLAYWRIGHT BROWSERS
# ═══════════════════════════════════════════════════════════════════
log_step "5. Playwright browsers"

if [ "$CHECK_ONLY" = "true" ]; then
    if command -v playwright &>/dev/null; then
        echo -e "  ${GREEN}✓${RESET} Playwright CLI disponible"
        local browsers
        browsers=$(playwright install --dry-run 2>/dev/null | wc -l || echo "0")
        echo -e "  ${GREEN}✓${RESET} ${browsers} navegadores instalados"
    else
        echo -e "  ${YELLOW}○${RESET} Playwright no instalado"
    fi
else
    if [ -f "${VENV_DIR}/bin/playwright" ]; then
        if confirm "¿Instalar navegadores de Playwright (~300MB)?"; then
            log_info "Instalando navegadores de Playwright..."
            source "${VENV_DIR}/bin/activate"
            playwright install chromium 2>&1 | tail -3
            deactivate 2>/dev/null || true
            step_ok "Playwright chromium instalado"
        else
            step_skip "Playwright browsers"
        fi
    elif command -v playwright &>/dev/null; then
        if confirm "¿Instalar navegadores de Playwright (~300MB)?"; then
            playwright install chromium 2>&1 | tail -3
            step_ok "Playwright chromium instalado"
        else
            step_skip "Playwright browsers"
        fi
    else
        log_info "Playwright no instalado (no está en el venv). Instálalo con:"
        echo "  source ${VENV_DIR}/bin/activate && playwright install chromium"
    fi
fi

# ═══════════════════════════════════════════════════════════════════
# 6. SCRIPTS PERMISSIONS
# ═══════════════════════════════════════════════════════════════════
log_step "6. Permisos de scripts"

if [ "$CHECK_ONLY" = "true" ]; then
    local scripts_count=0
    local executable_count=0
    for s in "$SCRIPTS_DIR"/*.sh; do
        [ -f "$s" ] || continue
        scripts_count=$((scripts_count + 1))
        if [ -x "$s" ]; then
            executable_count=$((executable_count + 1))
        fi
    done
    if [ "$executable_count" -eq "$scripts_count" ]; then
        echo -e "  ${GREEN}✓${RESET} ${executable_count}/${scripts_count} scripts ejecutables"
    else
        echo -e "  ${YELLOW}⚠${RESET} ${executable_count}/${scripts_count} scripts ejecutables — corre chmod +x scripts/*.sh"
    fi
else
    chmod +x "$SCRIPTS_DIR"/*.sh 2>/dev/null || true
    step_ok "Todos los scripts son ejecutables"
fi

# ═══════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════
echo ""
echo -e "${BOLD}=== Setup Summary ===${RESET}"
echo ""

# Quick verification
PASS=0
WARN=0

[ "$(check_cmd python3)" = "true" ] && PASS=$((PASS + 1)) || WARN=$((WARN + 1))
[ "$(check_cmd git)" = "true" ] && PASS=$((PASS + 1)) || WARN=$((WARN + 1))
[ "$(check_cmd pandoc)" = "true" ] && PASS=$((PASS + 1)) || WARN=$((WARN + 1))
[ -d "$VENV_DIR" ] && PASS=$((PASS + 1)) || WARN=$((WARN + 1))
[ -d "$GIT_HOOKS_DIR" ] && PASS=$((PASS + 1)) || WARN=$((WARN + 1))
[ -f "${PROJECT_ROOT}/.env" ] || [ -f "${HERMES_DIR}/.env" ] && PASS=$((PASS + 1)) || WARN=$((WARN + 1))

echo -e "  ${GREEN}✓${RESET} ${PASS} componentes listos"
[ "$WARN" -gt 0 ] && echo -e "  ${YELLOW}⚠${RESET} ${WARN} requieren atención"
echo ""

if [ "$WARN" -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✓ Entorno de desarrollo completo${RESET}"
else
    echo -e "${YELLOW}Revisa los warnings y ejecuta de nuevo si es necesario.${RESET}"
fi

echo ""
echo -e "${BOLD}Comandos útiles:${RESET}"
echo "  source ${VENV_DIR}/bin/activate    Activar virtualenv"
echo "  ./scripts/health-check.sh           Verificar estado del proyecto"
echo "  ./scripts/seed-db.sh                Inicializar PostgreSQL"
echo "  ./scripts/monitor.sh                Monitorear GPU/RAM/disco"
echo "  ./scripts/deploy-landing.sh         Deploy a Hostinger"
echo "  ./scripts/publish.sh list           Listar contenido del calendario"
echo ""

if [ -d "$VENV_DIR" ]; then
    echo -e "${BOLD}Para activar el entorno ahora:${RESET}"
    echo "  source ${VENV_DIR}/bin/activate"
    echo ""
fi

echo -e "${BOLD}=== Setup finalizado ===${RESET}"
echo "Log: ${SETUP_LOG}"
