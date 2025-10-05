#!/usr/bin/env bash

DRY_RUN=false

# Check if dry-run mode is enabled
if [[ "$QUICKGET_DRY_RUN" == "1" ]]; then
        DRY_RUN=true
fi

# Find the real curl
REAL_CURL="@curl@/bin/curl"

# Parse arguments to find output file and URL
OUTPUT_FILE=""
URL=""
ARGS=("$@")

for i in "${!ARGS[@]}"; do
        arg="${ARGS[$i]}"
        if [[ "$arg" == "-o" || "$arg" == "-O" || "$arg" == "--output" ]]; then
                OUTPUT_FILE="${ARGS[$i + 1]}"
        fi
        # Grab URL (typically doesn't start with -)
        if [[ "$arg" != -* ]] && [[ "$arg" != "" ]] && [[ ! "$arg" =~ ^/ ]]; then
                URL="$arg"
        fi
done

# Check if it's an ISO or MSI file
if [[ "$URL" =~ \.(iso|msi)$ ]] || [[ "$OUTPUT_FILE" =~ \.(iso|msi)$ ]]; then
        if $DRY_RUN; then
                echo "[DRY-RUN] Would download: $URL -> ${OUTPUT_FILE:-stdout}" >&2
                # Create empty file if output specified
                if [[ -n "$OUTPUT_FILE" ]]; then
                        touch "$OUTPUT_FILE"
                fi
                exit 0
        else
                echo "[DOWNLOAD] $URL -> ${OUTPUT_FILE:-stdout}" >&2
        fi
fi

# Execute real curl
exec "$REAL_CURL" "$@"
