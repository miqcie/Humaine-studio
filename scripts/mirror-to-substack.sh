#!/bin/bash
#
# Mirror a Jekyll post to Substack with formatted content and checklist.
#
# Usage:
#   ./scripts/mirror-to-substack.sh _posts/2026-03-02-my-post.md
#   ./scripts/mirror-to-substack.sh "https://humaine.studio/posts/2026/03/02/my-post/"
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -z "$1" ]; then
  echo "Usage:"
  echo "  ./scripts/mirror-to-substack.sh _posts/2026-03-02-my-post.md"
  echo "  ./scripts/mirror-to-substack.sh \"https://humaine.studio/...\""
  exit 1
fi

INPUT="$1"

if [[ "$INPUT" == http* ]]; then
  # URL mode (legacy)
  POST_URL="$INPUT"
  POST_TITLE=$(echo "$POST_URL" | sed 's/.*\/\([^/]*\)\/*$/\1/' | tr '-' ' ')

  echo ""
  echo "  Substack Mirror: $POST_TITLE"
  echo ""
  echo "  Checklist:"
  echo "  [ ] Copy content from: $POST_URL"
  echo "  [ ] Paste into Substack editor"
  echo "  [ ] Add email-friendly opening hook"
  echo "  [ ] Add footer: Originally published at $POST_URL"
  echo "  [ ] Set canonical URL: $POST_URL"
  echo "      (Settings > This post was originally published elsewhere)"
  echo "  [ ] Publish"
  echo ""
else
  # File mode
  POST_FILE="$INPUT"
  [[ "$POST_FILE" = /* ]] || POST_FILE="$PROJECT_DIR/$POST_FILE"

  if [ ! -f "$POST_FILE" ]; then
    echo "Error: File not found: $POST_FILE"
    exit 1
  fi

  POST_TITLE=$(grep '^title:' "$POST_FILE" | head -1 | sed 's/^title: *//; s/^"//; s/"$//')
  OUTPUT_DIR=$(mktemp -d)

  python3 "$SCRIPT_DIR/format-for-platforms.py" "$POST_FILE" \
    --platform substack --output-dir "$OUTPUT_DIR" 2>/dev/null

  BASENAME=$(basename "$POST_FILE" .md)
  FORMATTED="$OUTPUT_DIR/${BASENAME}-substack.md"
  CANONICAL_URL=$(grep "^Canonical URL:" "$FORMATTED" | sed 's/^Canonical URL: *//')

  echo ""
  echo "  Substack Mirror: $POST_TITLE"
  echo ""
  echo "  Formatted content: $FORMATTED"
  echo "  Canonical URL:     $CANONICAL_URL"
  echo ""
  echo "  Steps:"
  echo "  1. Open: https://humainestudio.substack.com/publish/post"
  echo "  2. Paste content from formatted file (skip metadata block)"
  echo "  3. Set canonical URL in post settings"
  echo "  4. Publish"
  echo ""
fi
