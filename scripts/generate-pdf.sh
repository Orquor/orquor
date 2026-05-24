#!/bin/bash
# generate-pdf.sh — Convert any .md file in the project to PDF via pandoc + xelatex
# Usage: ./scripts/generate-pdf.sh <path-to-markdown-file> [--output <output-path>] [--open]
#
# Requirements:
#   - pandoc (sudo apt install pandoc)
#   - texlive-xetex (sudo apt install texlive-xetex)
#   - Optional: texlive-latex-extra for additional LaTeX packages
#
# Examples:
#   ./scripts/generate-pdf.sh 03-whitepaper-acto/whitepaper-acto.md
#   ./scripts/generate-pdf.sh 03-whitepaper-acto/whitepaper-acto.md --output ./output/whitepaper.pdf
#   ./scripts/generate-pdf.sh 09-content-calendar/newsletter/edition-05.md --open
#   ./scripts/generate-pdf.sh 09-content-calendar/email/outreach-prospects.md

set -euo pipefail

# ─── Colors ────────────────────────────────────────────────────────
BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
RESET="\033[0m"

log_info()  { echo -e "${BLUE}[generate-pdf]${RESET} $1"; }
log_ok()    { echo -e "${GREEN}[generate-pdf]${RESET} $1"; }
log_warn()  { echo -e "${YELLOW}[generate-pdf]${RESET} $1"; }
log_error() { echo -e "${RED}[generate-pdf]${RESET} $1"; }

# ─── Paths ─────────────────────────────────────────────────────────
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT_DIR="${PROJECT_ROOT}/output"
TEMP_DIR="${PROJECT_ROOT}/.pdf-tmp"

# ─── Usage ─────────────────────────────────────────────────────────
usage() {
    echo -e "${BOLD}ORQUOR — Markdown to PDF Converter${RESET}"
    echo ""
    echo "Usage: $0 <markdown-file> [options]"
    echo ""
    echo "Arguments:"
    echo "  <markdown-file>     Path to the .md file (relative to project root or absolute)"
    echo ""
    echo "Options:"
    echo "  --output <path>     Specify output PDF path (default: output/<basename>.pdf)"
    echo "  --open              Open the PDF after generation (xdg-open / wslview)"
    echo "  --toc               Generate a table of contents"
    echo "  --help, -h          Show this help"
    echo ""
    echo "Requirements:"
    echo "  pandoc             Markdown to PDF converter"
    echo "  xelatex            XeLaTeX engine (included in texlive-xetex)"
    echo ""
    echo "Examples:"
    echo "  $0 03-whitepaper-acto/whitepaper-acto.md"
    echo "  $0 09-content-calendar/newsletter/edition-05.md --toc --open"
    echo "  $0 09-content-calendar/email/outreach-prospects.md --output ~/Desktop/demo.pdf"
    exit "${1:-0}"
}

# ─── Parse arguments ───────────────────────────────────────────────
INPUT_FILE=""
OUTPUT_FILE=""
OPEN_PDF="false"
GENERATE_TOC="false"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h)
            usage 0
            ;;
        --output)
            if [[ $# -lt 2 ]]; then
                log_error "--output requires a path argument."
                usage 1
            fi
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --open)
            OPEN_PDF="true"
            shift
            ;;
        --toc)
            GENERATE_TOC="true"
            shift
            ;;
        -*)
            log_error "Unknown option: $1"
            usage 1
            ;;
        *)
            if [ -z "$INPUT_FILE" ]; then
                INPUT_FILE="$1"
            else
                log_error "Unexpected argument: $1"
                usage 1
            fi
            shift
            ;;
    esac
done

if [ -z "$INPUT_FILE" ]; then
    log_error "No markdown file specified."
    usage 1
fi

# ─── Resolve input path ────────────────────────────────────────────
# If the path is relative and does not start with /, ./ or ../, treat as relative to PROJECT_ROOT
if [[ "$INPUT_FILE" != /* ]] && [[ "$INPUT_FILE" != ./* ]] && [[ "$INPUT_FILE" != ../* ]]; then
    INPUT_FILE="${PROJECT_ROOT}/${INPUT_FILE}"
fi

# Normalize to absolute path
INPUT_FILE="$(cd "$(dirname "$INPUT_FILE")" 2>/dev/null && pwd)/$(basename "$INPUT_FILE")" || {
    log_error "Cannot resolve input path: $INPUT_FILE"
    exit 1
}

if [ ! -f "$INPUT_FILE" ]; then
    log_error "Markdown file not found: $INPUT_FILE"
    exit 1
fi

if [[ ! "$INPUT_FILE" =~ \.md$ ]]; then
    log_warn "Input file does not have a .md extension: $INPUT_FILE"
    log_warn "Proceeding anyway, but results may vary."
fi

# ─── Resolve output path ───────────────────────────────────────────
INPUT_BASENAME="$(basename "$INPUT_FILE" .md)"
INPUT_DIR="$(dirname "$INPUT_FILE")"

if [ -z "$OUTPUT_FILE" ]; then
    # Default: output/<parent-dir>--<basename>.pdf
    mkdir -p "$OUTPUT_DIR"
    REL_PATH="${INPUT_FILE#$PROJECT_ROOT/}"
    # Convert slashes to double-dashes for a flat filename that preserves structure
    SAFE_NAME="$(echo "$REL_PATH" | sed 's|/|--|g' | sed 's|\.md$||').pdf"
    OUTPUT_FILE="${OUTPUT_DIR}/${SAFE_NAME}"
fi

# Ensure output is absolute
if [[ "$OUTPUT_FILE" != /* ]]; then
    OUTPUT_FILE="${PROJECT_ROOT}/${OUTPUT_FILE}"
fi

mkdir -p "$(dirname "$OUTPUT_FILE")"

# ─── Prerequisites check ───────────────────────────────────────────
MISSING_DEPS=""

if ! command -v pandoc &>/dev/null; then
    MISSING_DEPS="${MISSING_DEPS}  pandoc\n"
fi

if ! command -v xelatex &>/dev/null; then
    MISSING_DEPS="${MISSING_DEPS}  xelatex (install texlive-xetex)\n"
fi

if [ -n "$MISSING_DEPS" ]; then
    log_error "Missing dependencies:"
    echo -e "$MISSING_DEPS"
    echo ""
    echo "Install with:"
    echo "  sudo apt update"
    echo "  sudo apt install pandoc texlive-xetex texlive-latex-extra"
    exit 1
fi

# ─── Generate PDF ──────────────────────────────────────────────────
echo -e "${BOLD}=== ORQUOR — Markdown to PDF ===${RESET}"
echo ""
log_info "Input:   ${INPUT_FILE}"
log_info "Output:  ${OUTPUT_FILE}"

# Determine working directory for relative image paths
WORK_DIR="$(dirname "$INPUT_FILE")"

# Build pandoc arguments
PANDOC_ARGS=(
    --from=markdown+smart
    --pdf-engine=xelatex
    -V mainfont="DejaVu Serif"
    -V monofont="DejaVu Sans Mono"
    -V fontsize="11pt"
    -V geometry:margin=2.5cm
    -V colorlinks=true
    -V linkcolor=blue
    -V urlcolor=blue
    -V citecolor=blue
    -V toccolor=blue
)

if [ "$GENERATE_TOC" = "true" ]; then
    PANDOC_ARGS+=(--toc --toc-depth=3 -V toc-title="Índice")
fi

# Convert title/filename to a reasonable LaTeX title
TITLE_FROM_H1=$(head -20 "$INPUT_FILE" | grep -m1 '^# ' | sed 's/^# //' || echo "$INPUT_BASENAME")
PANDOC_ARGS+=(-V title="$TITLE_FROM_H1")

log_info "Engine:  xelatex"
log_info "Title:   $TITLE_FROM_H1"
[ "$GENERATE_TOC" = "true" ] && log_info "TOC:     yes (depth 3)"

echo ""
log_info "Running pandoc..."

START_TIME=$(date +%s)

pandoc "${PANDOC_ARGS[@]}" \
    -o "$OUTPUT_FILE" \
    "$INPUT_FILE" \
    --metadata date="$(date +%Y-%m-%d)"

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# ─── Verify output ─────────────────────────────────────────────────
if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo ""
    log_ok "PDF generated successfully!  (${DURATION}s, ${FILE_SIZE})"
    echo ""
    echo -e "  ${BOLD}Output:${RESET} ${OUTPUT_FILE}"

    # Open if requested
    if [ "$OPEN_PDF" = "true" ]; then
        echo ""
        log_info "Opening PDF..."
        if command -v wslview &>/dev/null; then
            wslview "$OUTPUT_FILE" &
        elif command -v xdg-open &>/dev/null; then
            xdg-open "$OUTPUT_FILE" &
        elif command -v open &>/dev/null; then
            open "$OUTPUT_FILE" &
        else
            log_warn "Cannot open PDF: no xdg-open, wslview, or open found."
        fi
    fi

    echo -e "${BOLD}=== Done ===${RESET}"
else
    echo ""
    log_error "PDF generation failed. No output file produced."
    log_error "Check pandoc/xelatex output above for errors."

    # Clean up any partial file
    rm -f "$OUTPUT_FILE"
    exit 1
fi

# ─── Clean up temp dir if empty ────────────────────────────────────
if [ -d "$TEMP_DIR" ] && [ -z "$(ls -A "$TEMP_DIR" 2>/dev/null)" ]; then
    rmdir "$TEMP_DIR" 2>/dev/null || true
fi
