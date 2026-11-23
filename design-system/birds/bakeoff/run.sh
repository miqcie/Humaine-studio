#!/bin/bash
# Run one vote round's drafts, tracing or blind sheets with their dependencies (Codex CLI must be logged in).
# usage: design-system/birds/bakeoff/run.sh [--dir round2] gen|trace|sheets
set -euo pipefail
cd "$(dirname "$0")"
exec uv run --quiet --with pillow --with numpy --with scipy --with fonttools --with brotli python run.py "$@"
