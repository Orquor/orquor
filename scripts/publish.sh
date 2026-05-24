#!/bin/bash
# publish.sh — ORQUOR Content Publication Automation
# Usage: ./scripts/publish.sh [channel] [date|id] [--dry-run]
# Manages the 90-day content calendar publication workflow.
#
# Channels: linkedin | x | youtube | newsletter | email
# Date/ID:   dia-NNN for social, ep-NNN for youtube, edition-NN for newsletter
#
# Examples:
#   ./scripts/publish.sh linkedin dia-001           # Publish LinkedIn dia-001
#   ./scripts/publish.sh x dia-014 --dry-run        # Preview X post dia-014
#   ./scripts/publish.sh youtube ep-001             # Publish YouTube episode
#   ./scripts/publish.sh newsletter edition-01      # Publish newsletter
#   ./scripts/publish.sh list                       # List all content + status
#   ./scripts/publish.sh status                     # Show publication progress

set -euo pipefail

# ─── Configuration ───────────────────────────────────────────────
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONTENT_DIR="${PROJECT_ROOT}/09-content-calendar"
PUBLISH_LOG="${PROJECT_ROOT}/.publish_log.json"

# Color output
BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
RESET="\033[0m"

# ─── Helpers ─────────────────────────────────────────────────────
log_info()  { echo -e "${BLUE}[publish]${RESET} $1"; }
log_ok()    { echo -e "${GREEN}[publish]${RESET} $1"; }
log_warn()  { echo -e "${YELLOW}[publish]${RESET} $1"; }
log_error() { echo -e "${RED}[publish]${RESET} $1"; }

init_log() {
    if [ ! -f "$PUBLISH_LOG" ]; then
        echo '{"published": {}, "last_updated": ""}' > "$PUBLISH_LOG"
    fi
}

mark_published() {
    local channel="$1" id="$2"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    python3 -c "
import json, sys
with open('$PUBLISH_LOG', 'r') as f:
    log = json.load(f)
log['published'].setdefault('$channel', {})['$id'] = '$timestamp'
log['last_updated'] = '$timestamp'
with open('$PUBLISH_LOG', 'w') as f:
    json.dump(log, f, indent=2)
"
}

is_published() {
    python3 -c "
import json
try:
    with open('$PUBLISH_LOG', 'r') as f:
        log = json.load(f)
    pub = log.get('published', {}).get('$1', {})
    sys.exit(0 if '$2' in pub else 1)
except Exception:
    sys.exit(1)
"
}

# ─── Content resolution ──────────────────────────────────────────
resolve_path() {
    local channel="$1" id="$2"
    local path=""

    case "$channel" in
        linkedin)   path="${CONTENT_DIR}/linkedin/${id}.md" ;;
        x)          path="${CONTENT_DIR}/x-twitter/${id}.md" ;;
        twitter)    path="${CONTENT_DIR}/x-twitter/${id}.md" ;;
        youtube)    path="${CONTENT_DIR}/youtube/${id}.md" ;;
        newsletter) path="${CONTENT_DIR}/newsletter/${id}.md" ;;
        email)
            # Email templates are in the email/ subfolder
            path="${CONTENT_DIR}/email/${id}.md"
            ;;
        *)
            log_error "Unknown channel: $channel"
            echo "Valid channels: linkedin, x, youtube, newsletter, email"
            exit 1
            ;;
    esac

    if [ ! -f "$path" ]; then
        log_error "Content file not found: $path"
        exit 1
    fi

    echo "$path"
}

# ─── Content validation ──────────────────────────────────────────
validate_content() {
    local path="$1"
    local errors=0

    # Check file is not empty
    if [ ! -s "$path" ]; then
        log_error "Empty file: $path"
        errors=$((errors + 1))
    fi

    # Check for required metadata (title-like first line)
    local first_line
    first_line=$(head -1 "$path")
    if [[ ! "$first_line" =~ ^# ]]; then
        log_warn "Missing H1 title in: $path"
    fi

    # Check character count for social platforms
    local channel="$2"
    local char_count
    char_count=$(wc -m < "$path")

    case "$channel" in
        x|twitter)
            if [ "$char_count" -gt 2800 ]; then
                log_warn "X post exceeds ~2800 chars ($char_count chars) — may need thread splitting"
            fi
            ;;
        linkedin)
            if [ "$char_count" -gt 15000 ]; then
                log_warn "LinkedIn post exceeds ~15000 chars ($char_count chars) — may get truncated"
            fi
            ;;
    esac

    return $errors
}

# ─── Preview ─────────────────────────────────────────────────────
preview_content() {
    local path="$1"
    echo -e "${BOLD}━━━ PREVIEW: $(basename "$path") ━━━${RESET}"
    echo ""
    cat "$path"
    echo ""
    echo -e "${BOLD}━━━ END PREVIEW ━━━${RESET}"
}

# ─── Publish actions ─────────────────────────────────────────────
publish_content() {
    local channel="$1" id="$2" dry="$3"
    local path
    path=$(resolve_path "$channel" "$id")

    # Validate
    validate_content "$path" "$channel" || {
        log_error "Validation failed. Fix issues before publishing."
        exit 1
    }

    # Check if already published
    if is_published "$channel" "$id"; then
        log_warn "Already published: $channel / $id"
        log_info "Use --force to re-publish (not implemented yet)."
        exit 0
    fi

    echo ""
    log_info "Channel:   $channel"
    log_info "Content:   $id"
    log_info "File:      $path"
    log_info "Chars:     $(wc -m < "$path")"
    echo ""

    if [ "$dry" = "true" ]; then
        log_warn "DRY RUN — content will NOT be published."
        preview_content "$path"
        log_ok "Dry run complete. Remove --dry-run to publish."
        return
    fi

    # Confirm before live publish
    preview_content "$path"
    echo ""
    echo -ne "${YELLOW}Publish this content to $channel? [y/N] ${RESET}"
    read -r confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        log_info "Publish cancelled."
        exit 0
    fi

    # Mark as published
    mark_published "$channel" "$id"

    log_ok "Content marked as published: $channel / $id"
    echo ""

    # Platform-specific instructions
    case "$channel" in
        linkedin)
            echo "→ Copy the content above and paste into LinkedIn."
            echo "→ Target: Orquor Company Page + founder's personal profile."
            ;;
        x|twitter)
            echo "→ Copy the content above and post to @orquor on X."
            echo "→ If thread: paste each tweet sequentially with reply chaining."
            ;;
        youtube)
            echo "→ Use this script as the recording guide."
            echo "→ Upload to youtube.com/@orquor when recording is complete."
            ;;
        newsletter)
            echo "→ Copy into your newsletter platform (Substack, Mailchimp, etc.)."
            echo "→ Schedule for the date indicated in 09-content-calendar/CALENDAR.md."
            ;;
        email)
            echo "→ Use this template in your email client."
            echo "→ Personalize recipient-specific fields before sending."
            ;;
    esac
}

# ─── List / status ────────────────────────────────────────────────
list_all() {
    echo -e "${BOLD}ORQUOR Content Calendar — Publication Status${RESET}"
    echo ""

    for channel_dir in "${CONTENT_DIR}"/*/; do
        local channel
        channel=$(basename "$channel_dir")
        local count
        count=$(find "$channel_dir" -maxdepth 1 -name '*.md' ! -name 'CALENDAR.md' 2>/dev/null | wc -l)
        if [ "$count" -eq 0 ]; then continue; fi

        local published_count=0
        for f in "$channel_dir"/*.md; do
            [ -f "$f" ] || continue
            local id
            id=$(basename "$f" .md)
            if is_published "$channel" "$id" 2>/dev/null; then
                published_count=$((published_count + 1))
            fi
        done

        local pct=0
        if [ "$count" -gt 0 ]; then
            pct=$((published_count * 100 / count))
        fi

        printf "  %-15s  %2d/%2d published  (%d%%)" "$channel" "$published_count" "$count" "$pct"
        if [ "$pct" -eq 100 ]; then
            echo -e "  ${GREEN}✓ complete${RESET}"
        elif [ "$pct" -gt 0 ]; then
            echo -e "  ${YELLOW}→ in progress${RESET}"
        else
            echo -e "  ${BLUE}○ pending${RESET}"
        fi
    done

    echo ""
    echo "Master calendar: ${CONTENT_DIR}/CALENDAR.md"
}

# ─── Main ─────────────────────────────────────────────────────────
main() {
    init_log

    local channel="${1:-}"
    local id="${2:-}"
    local dry="false"

    # Parse flags
    for arg in "$@"; do
        case "$arg" in
            --dry-run) dry="true" ;;
        esac
    done

    case "$channel" in
        list|status)
            list_all
            ;;
        linkedin|x|twitter|youtube|newsletter|email)
            if [ -z "$id" ]; then
                log_error "Missing content ID. Usage: $0 $channel <dia-NNN|ep-NNN|edition-NN|template-name>"
                echo ""
                echo "Available content for $channel:"
                local dir="${CONTENT_DIR}/${channel}"
                [ "$channel" = "x" ] && dir="${CONTENT_DIR}/x-twitter"
                [ "$channel" = "twitter" ] && dir="${CONTENT_DIR}/x-twitter"
                find "$dir" -maxdepth 1 -name '*.md' ! -name 'CALENDAR.md' -exec basename {} .md \; 2>/dev/null | sort | head -20
                exit 1
            fi
            publish_content "$channel" "$id" "$dry"
            ;;
        *)
            echo "ORQUOR — Content Publication Script"
            echo ""
            echo "Usage: $0 <channel> <id> [--dry-run]"
            echo "       $0 list"
            echo ""
            echo "Channels:"
            echo "  linkedin     LinkedIn posts (dia-001 to dia-021)"
            echo "  x            X/Twitter posts (dia-001 to dia-014)"
            echo "  youtube      YouTube episode scripts (ep-001, ep-002)"
            echo "  newsletter   Newsletter editions (edition-01)"
            echo "  email        Email templates (onboarding-interpretes, welcome-clientes-b2b, follow-up-prospects)"
            echo ""
            echo "Options:"
            echo "  --dry-run    Preview content without marking as published"
            echo ""
            echo "Examples:"
            echo "  $0 linkedin dia-001"
            echo "  $0 x dia-014 --dry-run"
            echo "  $0 list"
            ;;
    esac
}

main "$@"
