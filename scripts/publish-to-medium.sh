#!/bin/bash
#
# Publish a Jekyll post to Medium via Import Story.
#
# Medium's API is deprecated and no longer issues tokens.
# This script formats content and guides you through Import Story.
#
# Usage:
#   ./scripts/publish-to-medium.sh _posts/2026-03-02-my-post.md
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -z "$1" ]; then
  echo "Usage:"
  echo "  ./scripts/publish-to-medium.sh _posts/2026-03-02-my-post.md"
  exit 1
fi

POST_FILE="$1"
[[ "$POST_FILE" = /* ]] || POST_FILE="$PROJECT_DIR/$POST_FILE"

if [ ! -f "$POST_FILE" ]; then
  echo "Error: File not found: $POST_FILE"
  exit 1
fi

POST_TITLE=$(grep '^title:' "$POST_FILE" | head -1 | sed 's/^title: *//; s/^"//; s/"$//')
OUTPUT_DIR=$(mktemp -d)

python3 "$SCRIPT_DIR/format-for-platforms.py" "$POST_FILE" \
  --platform medium --output-dir "$OUTPUT_DIR" 2>/dev/null

BASENAME=$(basename "$POST_FILE" .md)
FORMATTED="$OUTPUT_DIR/${BASENAME}-medium.md"
CANONICAL_URL=$(grep "^Canonical URL:" "$FORMATTED" | sed 's/^Canonical URL: *//')
TAGS=$(grep "^Tags:" "$FORMATTED" | sed 's/^Tags: *//')

echo ""
echo "  Medium Publisher: $POST_TITLE"
echo ""
echo "  Import Story (recommended):"
echo "  1. Medium > Profile > Stories > Import a story"
echo "  2. Paste URL: $CANONICAL_URL"
echo "  3. Medium auto-imports content + sets canonical URL"
echo "  4. Add tags: $TAGS"
echo "  5. Review and publish"
echo ""
echo "  Or paste formatted content from: $FORMATTED"
echo ""
