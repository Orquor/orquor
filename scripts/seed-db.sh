#!/bin/bash
# seed-db.sh — Inicializa PostgreSQL con el esquema completo de ORQUOR
# Uso: ./scripts/seed-db.sh [--reset|--check|--migrate]
#
# REQUISITOS:
#   - psql (cliente PostgreSQL) instalado
#   - Variables de entorno (en .env):
#       DATABASE_URL  — URL de conexión PostgreSQL
#
# Modos:
#   (default)     Crea tablas + índices si no existen (idempotente)
#   --reset       ELIMINA y recrea toda la base de datos (¡peligroso!)
#   --check       Solo verifica conectividad y existencia de tablas
#   --migrate     Ejecuta migraciones pendientes (migrations/*.sql)
#
# Esquema incluido:
#   1. sessions        — Sesiones clínicas ACTO
#   2. audit_log       — Registro de auditoría por utterance
#   3. memory_entries  — Memoria compartida del orchestrator
#   4. feedback_events — Eventos de feedback de sub-agents
#   5. content_calendar — Calendario de contenido y publicaciones
#   6. prospects       — Tracking de prospects/leads
#   7. ops_metrics     — Métricas operacionales (GPU, latencia, etc.)

set -euo pipefail

# ─── Colors ────────────────────────────────────────────────────────
BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
RESET="\033[0m"

log_info()  { echo -e "${BLUE}[seed-db]${RESET} $1"; }
log_ok()    { echo -e "${GREEN}[seed-db]${RESET} $1"; }
log_warn()  { echo -e "${YELLOW}[seed-db]${RESET} $1"; }
log_error() { echo -e "${RED}[seed-db]${RESET} $1"; }

# ─── Paths ─────────────────────────────────────────────────────────
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MIGRATIONS_DIR="${PROJECT_ROOT}/migrations"
SCHEMA_FILE="${MIGRATIONS_DIR}/001_schema.sql"

# ─── Parse args ────────────────────────────────────────────────────
MODE="seed"
for arg in "$@"; do
    case "$arg" in
        --reset)   MODE="reset" ;;
        --check)   MODE="check" ;;
        --migrate) MODE="migrate" ;;
        --help|-h)
            echo "Uso: $0 [--reset|--check|--migrate]"
            echo ""
            echo "  (default)   Crea tablas si no existen (idempotente)"
            echo "  --reset     ELIMINA y recrea TODO (¡datos se pierden!)"
            echo "  --check     Verifica conectividad + tablas existentes"
            echo "  --migrate   Ejecuta migraciones pendientes en migrations/"
            echo ""
            echo "Requiere DATABASE_URL en .env"
            exit 0
            ;;
        *)
            log_error "Opción desconocida: $arg"
            exit 1
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

if [ -z "${DATABASE_URL:-}" ]; then
    log_error "DATABASE_URL no definida. Configúrala en .env"
    echo "  Ejemplo: DATABASE_URL=postgresql://orquor:***@localhost:5432/orquor_hermes"
    exit 1
fi

# ─── Check psql ────────────────────────────────────────────────────
if ! command -v psql &>/dev/null; then
    log_error "psql no encontrado. Instálalo con: sudo apt install postgresql-client"
    exit 1
fi

# ─── Connection helper ─────────────────────────────────────────────
PSQL_CMD="psql ${DATABASE_URL}"

db_exec() {
    $PSQL_CMD -c "$1" 2>&1 || {
        log_error "Error ejecutando SQL: $1"
        return 1
    }
}

db_exec_quiet() {
    $PSQL_CMD -q -t -c "$1" 2>/dev/null || echo ""
}

# ─── Test connectivity ─────────────────────────────────────────────
test_connection() {
    local result
    result=$(db_exec_quiet "SELECT 1;" 2>&1)
    if [ "$result" = "1" ]; then
        return 0
    else
        return 1
    fi
}

echo -e "${BOLD}=== ORQUOR PostgreSQL Setup ===${RESET}"
echo ""

# ─── Connection test ───────────────────────────────────────────────
log_info "Probando conexión a PostgreSQL..."
if test_connection; then
    log_ok "Conexión exitosa a PostgreSQL"
else
    log_error "No se pudo conectar a PostgreSQL con DATABASE_URL"
    echo ""
    echo "Verifica:"
    echo "  1. PostgreSQL está corriendo (pg_isready)"
    echo "  2. La URL es correcta: ${DATABASE_URL}"
    echo "  3. El usuario y contraseña son válidos"
    echo "  4. La base de datos existe (crear con: createdb orquor_hermes)"
    exit 1
fi

echo ""

# ─── SCHEMA SQL (inline — también se escribe a migrations/) ────────
SCHEMA_SQL="
-- ============================================================
-- ORQUOR Database Schema v1.0
-- PostgreSQL 15+ con pgvector
-- ============================================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";
CREATE EXTENSION IF NOT EXISTS \"pgcrypto\";

-- Vector extension (para Qdrant, opcional en PostgreSQL)
DO \$\$
BEGIN
    CREATE EXTENSION IF NOT EXISTS vector;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'pgvector extension not available (optional, Qdrant handles vectors)';
END;
\$\$;

-- ============================================================
-- 1. SESSIONS — Sesiones clínicas ACTO
-- ============================================================
CREATE TABLE IF NOT EXISTS sessions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id     VARCHAR(64) NOT NULL,
    department      VARCHAR(64) NOT NULL,
    source_language VARCHAR(10) NOT NULL,
    target_language VARCHAR(10) NOT NULL,
    register        VARCHAR(32) NOT NULL DEFAULT 'formal_clinical',
    patient_id      VARCHAR(128),
    clinician_id    VARCHAR(128),
    consent_verified BOOLEAN NOT NULL DEFAULT false,
    consent_method  VARCHAR(32),
    status          VARCHAR(16) NOT NULL DEFAULT 'active',
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at       TIMESTAMPTZ,
    timezone        VARCHAR(64) DEFAULT 'America/Lima'
);

CREATE INDEX IF NOT EXISTS idx_sessions_customer ON sessions(customer_id);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);
CREATE INDEX IF NOT EXISTS idx_sessions_created ON sessions(created_at DESC);

-- ============================================================
-- 2. AUDIT_LOG — Registro de auditoría por utterance
-- ============================================================
CREATE TABLE IF NOT EXISTS audit_log (
    id              BIGSERIAL PRIMARY KEY,
    session_id      UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    utterance_id    INTEGER NOT NULL,
    timestamp       TIMESTAMPTZ NOT NULL DEFAULT now(),
    source_audio_ref VARCHAR(512),
    asr_transcript  TEXT,
    asr_confidence  DOUBLE PRECISION,
    asr_latency_ms  INTEGER,
    mt_translation  TEXT,
    mt_register     VARCHAR(32),
    mt_model        VARCHAR(64),
    mt_latency_ms   INTEGER,
    verifier_suite_version VARCHAR(16),
    verifier_results JSONB DEFAULT '[]',
    verifier_score  INTEGER,
    escalated       BOOLEAN NOT NULL DEFAULT false,
    human_correction TEXT,
    crypto_tsa      VARCHAR(32),
    crypto_token    TEXT,
    crypto_signature TEXT,
    raw_json        JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_audit_session ON audit_log(session_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_escalated ON audit_log(escalated) WHERE escalated = true;
CREATE INDEX IF NOT EXISTS idx_audit_verifier_score ON audit_log(verifier_score);

-- ============================================================
-- 3. MEMORY_ENTRIES — Memoria compartida del orchestrator
-- ============================================================
CREATE TABLE IF NOT EXISTS memory_entries (
    id              BIGSERIAL PRIMARY KEY,
    timestamp       TIMESTAMPTZ NOT NULL DEFAULT now(),
    sub_agent       VARCHAR(64) NOT NULL,
    feedback_type   VARCHAR(32) NOT NULL,
    section_affected VARCHAR(128),
    feedback_text   TEXT NOT NULL,
    canonical_rule  VARCHAR(64) NOT NULL,
    verdict         VARCHAR(32) NOT NULL,
    action_taken    TEXT NOT NULL,
    reasoning       TEXT,
    outcome         TEXT,
    task_id         VARCHAR(64),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_memory_agent ON memory_entries(sub_agent);
CREATE INDEX IF NOT EXISTS idx_memory_timestamp ON memory_entries(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_memory_verdict ON memory_entries(verdict);

-- ============================================================
-- 4. FEEDBACK_EVENTS — Eventos de feedback de sub-agents
-- ============================================================
CREATE TABLE IF NOT EXISTS feedback_events (
    id              BIGSERIAL PRIMARY KEY,
    source          VARCHAR(32) NOT NULL,
    sub_agent       VARCHAR(64) NOT NULL,
    feedback_text   TEXT NOT NULL,
    verdict         VARCHAR(32) NOT NULL,
    action_taken    TEXT,
    task_id         VARCHAR(64),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_feedback_source ON feedback_events(source);
CREATE INDEX IF NOT EXISTS idx_feedback_agent ON feedback_events(sub_agent);
CREATE INDEX IF NOT EXISTS idx_feedback_created ON feedback_events(created_at DESC);

-- ============================================================
-- 5. CONTENT_CALENDAR — Calendario de contenido y publicaciones
-- ============================================================
CREATE TABLE IF NOT EXISTS content_calendar (
    id              BIGSERIAL PRIMARY KEY,
    channel         VARCHAR(16) NOT NULL,
    content_id      VARCHAR(64) NOT NULL,
    title           VARCHAR(256),
    status          VARCHAR(16) NOT NULL DEFAULT 'draft',
    published_at    TIMESTAMPTZ,
    file_path       VARCHAR(512),
    char_count      INTEGER,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(channel, content_id)
);

CREATE INDEX IF NOT EXISTS idx_content_channel ON content_calendar(channel);
CREATE INDEX IF NOT EXISTS idx_content_status ON content_calendar(status);
CREATE INDEX IF NOT EXISTS idx_content_published ON content_calendar(published_at DESC);

-- ============================================================
-- 6. PROSPECTS — Tracking de prospects/leads
-- ============================================================
CREATE TABLE IF NOT EXISTS prospects (
    id              BIGSERIAL PRIMARY KEY,
    name            VARCHAR(256) NOT NULL,
    company         VARCHAR(256),
    role            VARCHAR(128),
    email           VARCHAR(256),
    linkedin_url    VARCHAR(512),
    source          VARCHAR(64),
    stage           VARCHAR(32) NOT NULL DEFAULT 'discovered',
    notes           TEXT,
    last_contact    TIMESTAMPTZ,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_prospects_stage ON prospects(stage);
CREATE INDEX IF NOT EXISTS idx_prospects_company ON prospects(company);
CREATE INDEX IF NOT EXISTS idx_prospects_created ON prospects(created_at DESC);

-- ============================================================
-- 7. OPS_METRICS — Métricas operacionales
-- ============================================================
CREATE TABLE IF NOT EXISTS ops_metrics (
    id              BIGSERIAL PRIMARY KEY,
    metric_name     VARCHAR(64) NOT NULL,
    metric_value    DOUBLE PRECISION NOT NULL,
    unit            VARCHAR(16),
    component       VARCHAR(64),
    tags            JSONB DEFAULT '{}',
    recorded_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ops_name ON ops_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_ops_recorded ON ops_metrics(recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_ops_component ON ops_metrics(component);

-- Convert to hypertable if TimescaleDB available
DO \$\$
BEGIN
    PERFORM create_hypertable('ops_metrics', 'recorded_at', if_not_exists => true);
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'TimescaleDB not available — using standard table for ops_metrics';
END;
\$\$;

-- ============================================================
-- DEFAULT DATA — Valores iniciales
-- ============================================================
INSERT INTO content_calendar (channel, content_id, title, status)
VALUES
    ('linkedin', 'dia-001', 'Presentación de ORQUOR Clinical', 'draft'),
    ('email', 'onboarding-completo', 'Onboarding Completo Interpretes', 'draft'),
    ('email', 'outreach-prospects', 'Email Outreach Prospects', 'draft')
ON CONFLICT (channel, content_id) DO NOTHING;

-- ============================================================
-- VIEWS — Vistas útiles para reporting
-- ============================================================
CREATE OR REPLACE VIEW v_active_sessions AS
    SELECT * FROM sessions WHERE status = 'active';

CREATE OR REPLACE VIEW v_recent_audit AS
    SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 1000;

CREATE OR REPLACE VIEW v_escalation_rate AS
    SELECT
        date_trunc('hour', timestamp) AS hour,
        COUNT(*) AS total_utterances,
        SUM(CASE WHEN escalated THEN 1 ELSE 0 END) AS escalated,
        ROUND(SUM(CASE WHEN escalated THEN 1 ELSE 0 END)::numeric / NULLIF(COUNT(*), 0) * 100, 2) AS escalation_pct
    FROM audit_log
    WHERE timestamp > now() - INTERVAL '24 hours'
    GROUP BY hour
    ORDER BY hour DESC;

CREATE OR REPLACE VIEW v_gpu_metrics AS
    SELECT * FROM ops_metrics
    WHERE metric_name IN ('gpu_temp', 'gpu_util', 'gpu_mem')
    AND recorded_at > now() - INTERVAL '1 hour'
    ORDER BY recorded_at DESC;

CREATE OR REPLACE VIEW v_prospect_funnel AS
    SELECT stage, COUNT(*) AS count
    FROM prospects
    GROUP BY stage
    ORDER BY
        CASE stage
            WHEN 'discovered' THEN 1
            WHEN 'contacted' THEN 2
            WHEN 'in_conversation' THEN 3
            WHEN 'qualified' THEN 4
            WHEN 'proposal' THEN 5
            WHEN 'negotiation' THEN 6
            WHEN 'won' THEN 7
            WHEN 'lost' THEN 8
        END;

-- ============================================================
-- GRANTS — Permisos (ajustar según entorno)
-- ============================================================
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO orquor_app;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO orquor_app;
"

# ─── MODE: Check ───────────────────────────────────────────────────
check_mode() {
    echo -e "${BOLD}── Database Check ──${RESET}"
    echo ""

    local tables
    tables=$(db_exec_quiet "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public' ORDER BY tablename;" 2>/dev/null || echo "")

    if [ -z "$tables" ]; then
        log_warn "No hay tablas en el esquema public. Ejecuta: $0 (sin flags)"
        return 0
    fi

    echo -e "  ${BOLD}Tablas existentes:${RESET}"
    while IFS= read -r t; do
        [ -z "$t" ] && continue
        local count
        count=$(db_exec_quiet "SELECT COUNT(*) FROM \"$t\";" 2>/dev/null || echo "?")
        count=$(echo "$count" | xargs)
        echo -e "    ${GREEN}✓${RESET} ${t} (${count} filas)"
    done <<< "$tables"

    echo ""

    # Check views
    local views
    views=$(db_exec_quiet "SELECT viewname FROM pg_catalog.pg_views WHERE schemaname='public' ORDER BY viewname;" 2>/dev/null || echo "")
    if [ -n "$views" ]; then
        echo -e "  ${BOLD}Vistas:${RESET}"
        while IFS= read -r v; do
            [ -z "$v" ] && continue
            echo -e "    ${GREEN}✓${RESET} ${v}"
        done <<< "$views"
    fi

    echo ""
    log_ok "Check completado."
}

# ─── MODE: Reset ───────────────────────────────────────────────────
reset_mode() {
    echo -e "${RED}${BOLD}⚠ ATENCIÓN: Esto eliminará TODAS las tablas y datos ⚠${RESET}"
    echo ""
    echo -ne "${YELLOW}Escribe 'ELIMINAR TODO' para confirmar: ${RESET}"
    read -r confirm

    if [ "$confirm" != "ELIMINAR TODO" ]; then
        log_info "Reset cancelado."
        exit 0
    fi

    echo ""
    log_warn "Eliminando todas las tablas..."
    db_exec "DROP TABLE IF EXISTS
        ops_metrics,
        prospects,
        content_calendar,
        feedback_events,
        memory_entries,
        audit_log,
        sessions
    CASCADE;"

    log_warn "Eliminando vistas..."
    db_exec "DROP VIEW IF EXISTS
        v_active_sessions,
        v_recent_audit,
        v_escalation_rate,
        v_gpu_metrics,
        v_prospect_funnel
    CASCADE;"

    log_ok "Tablas eliminadas. Recreando esquema..."
    echo ""

    # Fall through to seed
    MODE="seed"
}

# ─── MODE: Seed / Create ───────────────────────────────────────────
seed_mode() {
    echo -e "${BOLD}── Creando esquema ORQUOR ──${RESET}"
    echo ""

    # Check if tables already exist
    local existing
    existing=$(db_exec_quiet "SELECT COUNT(*) FROM pg_catalog.pg_tables WHERE schemaname='public' AND tablename='sessions';" 2>/dev/null | xargs || echo "0")

    if [ "$existing" -gt 0 ]; then
        log_info "Tablas ya existen — ejecutando en modo idempotente (CREATE IF NOT EXISTS)"
    fi

    # Write schema to migrations dir
    mkdir -p "$MIGRATIONS_DIR"
    echo "$SCHEMA_SQL" > "$SCHEMA_FILE"
    log_info "Schema SQL guardado en: ${SCHEMA_FILE}"

    # Execute schema
    log_info "Ejecutando schema SQL..."
    echo "$SCHEMA_SQL" | $PSQL_CMD -q 2>&1 | while IFS= read -r line; do
        if [ -n "$line" ]; then
            echo "  $line"
        fi
    done

    local exec_status=${PIPESTATUS[0]}
    if [ "$exec_status" -eq 0 ]; then
        echo ""
        log_ok "Esquema creado exitosamente."

        # Verify
        echo ""
        log_info "Verificando tablas creadas:"
        local tables
        tables=$(db_exec_quiet "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public' ORDER BY tablename;" 2>/dev/null)
        while IFS= read -r t; do
            [ -z "$t" ] && continue
            echo -e "  ${GREEN}✓${RESET} ${t}"
        done <<< "$tables"
    else
        log_error "Error al ejecutar el schema SQL (exit code: $exec_status)"
        exit 1
    fi

    echo ""
    echo -e "${BOLD}=== Schema creado ===${RESET}"
    echo ""
    echo "Base de datos: ${DATABASE_URL}"
    echo "Migrations dir: ${MIGRATIONS_DIR}"
    echo ""
    echo "Comandos útiles:"
    echo "  $0 --check        Verificar estado de tablas"
    echo "  $0 --migrate      Ejecutar migraciones pendientes"
    echo "  psql ${DATABASE_URL}  Conectarse directamente"
}

# ─── MODE: Migrate ─────────────────────────────────────────────────
migrate_mode() {
    echo -e "${BOLD}── Ejecutando migraciones ──${RESET}"
    echo ""

    if [ ! -d "$MIGRATIONS_DIR" ]; then
        log_warn "Directorio de migraciones no encontrado: ${MIGRATIONS_DIR}"
        log_info "Creando schema base primero..."
        seed_mode
        return
    fi

    local migration_files
    migration_files=$(find "$MIGRATIONS_DIR" -name '*.sql' -type f | sort)

    if [ -z "$migration_files" ]; then
        log_warn "No se encontraron archivos .sql en ${MIGRATIONS_DIR}"
        return
    fi

    # Create migrations tracking table
    db_exec "CREATE TABLE IF NOT EXISTS _migrations (
        filename VARCHAR(256) PRIMARY KEY,
        applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );" 2>/dev/null || true

    local applied=0
    local skipped=0
    local failed=0

    while IFS= read -r migration; do
        [ -z "$migration" ] && continue
        local fname
        fname=$(basename "$migration")

        # Check if already applied
        local already
        already=$(db_exec_quiet "SELECT COUNT(*) FROM _migrations WHERE filename='$fname';" 2>/dev/null | xargs || echo "0")

        if [ "$already" -gt 0 ]; then
            log_info "Saltando (ya aplicada): ${fname}"
            skipped=$((skipped + 1))
            continue
        fi

        log_info "Aplicando: ${fname}..."

        if $PSQL_CMD -q -f "$migration" 2>&1; then
            db_exec "INSERT INTO _migrations (filename) VALUES ('$fname');" 2>/dev/null
            log_ok "  ✓ ${fname}"
            applied=$((applied + 1))
        else
            log_error "  ✗ ${fname} — FALLÓ"
            failed=$((failed + 1))
        fi
    done <<< "$migration_files"

    echo ""
    echo -e "  ${GREEN}Aplicadas: ${applied}${RESET}"
    [ "$skipped" -gt 0 ] && echo -e "  ${BLUE}Saltadas:  ${skipped}${RESET}"
    [ "$failed" -gt 0 ] && echo -e "  ${RED}Fallidas:  ${failed}${RESET}"

    if [ "$failed" -gt 0 ]; then
        exit 1
    fi

    log_ok "Migraciones completadas."
}

# ─── Dispatch ──────────────────────────────────────────────────────
case "$MODE" in
    check)
        check_mode
        ;;
    reset)
        reset_mode
        # If reset completed, also run seed
        if [ "$MODE" = "seed" ]; then
            seed_mode
        fi
        ;;
    seed)
        seed_mode
        ;;
    migrate)
        migrate_mode
        ;;
esac

echo ""
echo -e "${BOLD}=== DB Setup finalizado ===${RESET}"
