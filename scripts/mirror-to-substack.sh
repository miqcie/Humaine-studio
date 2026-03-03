#!/bin/bash
#
# Mirror a Jekyll post to Substack with formatted content and checklist.
#
# Two usage modes:
#   1. From post file (preferred) - formats content automatically
#   2. From URL (legacy) - opens browser with checklist
#
# Usage:
#   ./scripts/mirror-to-substack.sh _posts/2026-03-02-my-post.md
#   ./scripts/mirror-to-substack.sh "https://humaine.studio/posts/2026/03/02/my-post/"
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Check if argument provided
if [ -z "$1" ]; then
  echo "Error: Please provide a post file or URL"
  echo ""
  echo "Usage:"
  echo "  ./scripts/mirror-to-substack.sh _posts/2026-03-02-my-post.md"
  echo "  ./scripts/mirror-to-substack.sh \"https://humaine.studio/posts/2026/03/02/my-post/\""
  echo ""
  exit 1
fi

INPUT="$1"

# Determine if input is a file or URL
if [[ "$INPUT" == http* ]]; then
  # --- Legacy URL mode ---
  POST_URL="$INPUT"
  POST_TITLE=$(echo "$POST_URL" | sed 's/.*\/\([^/]*\)\/*$/\1/' | tr '-' ' ')

  echo ""
  echo "================================================================"
  echo "  Substack Mirroring Helper"
  echo "================================================================"
  echo ""
  echo "  Post: $POST_TITLE"
  echo "  Source URL: $POST_URL"
  echo ""

  # Try to open browser
  if command -v open &> /dev/null; then
    open "$POST_URL"
    sleep 1
    open "https://humainestudio.substack.com/publish/post"
    echo "  URLs opened in browser"
  elif command -v xdg-open &> /dev/null; then
    xdg-open "$POST_URL" 2>/dev/null &
    sleep 1
    xdg-open "https://humainestudio.substack.com/publish/post" 2>/dev/null &
    echo "  URLs opened in browser"
  else
    echo "  Open these URLs manually:"
    echo "    1. $POST_URL"
    echo "    2. https://humainestudio.substack.com/publish/post"
  fi

  echo ""
  echo "================================================================"
  echo "  Checklist:"
  echo "================================================================"
  echo ""
  echo "  [ ] Copy content from Jekyll post"
  echo "  [ ] Paste into Substack editor"
  echo "  [ ] Add email-friendly opening hook"
  echo "  [ ] Add footer: 'Originally published at [URL]'"
  echo "  [ ] Add call-to-action (subscribe, share, etc.)"
  echo "  [ ] Set canonical URL in post settings:"
  echo "      'This post was originally published elsewhere'"
  echo "      Canonical URL: $POST_URL"
  echo "  [ ] Preview post"
  echo "  [ ] Publish or schedule"
  echo ""
  echo "  Canonical URL (copy this):"
  echo "  $POST_URL"
  echo ""
else
  # --- File mode (preferred) ---
  POST_FILE="$INPUT"

  # Resolve relative path from project root
  if [[ ! "$POST_FILE" = /* ]]; then
    POST_FILE="$PROJECT_DIR/$POST_FILE"
  fi

  if [ ! -f "$POST_FILE" ]; then
    echo "Error: File not found: $POST_FILE"
    exit 1
  fi

  POST_TITLE=$(grep '^title:' "$POST_FILE" | head -1 | sed 's/^title: *//; s/^"//; s/"$//')

  echo ""
  echo "================================================================"
  echo "  Substack Mirroring Helper"
  echo "================================================================"
  echo ""
  echo "  Post: $POST_TITLE"
  echo ""

  # Generate formatted content
  OUTPUT_DIR=$(mktemp -d)
  python3 "$SCRIPT_DIR/format-for-platforms.py" "$POST_FILE" \
    --platform substack --output-dir "$OUTPUT_DIR" 2>/dev/null

  BASENAME=$(basename "$POST_FILE" .md)
  FORMATTED="$OUTPUT_DIR/${BASENAME}-substack.md"

  # Extract canonical URL from formatted output
  CANONICAL_URL=$(grep "^Canonical URL:" "$FORMATTED" | sed 's/^Canonical URL: *//')

  echo "  Formatted content saved to:"
  echo "  $FORMATTED"
  echo ""
  echo "================================================================"
  echo "  Publishing Steps:"
  echo "================================================================"
  echo ""
  echo "  1. Open Substack editor:"
  echo "     https://humainestudio.substack.com/publish/post"
  echo ""
  echo "  2. Copy content from the formatted file:"
  echo "     cat $FORMATTED"
  echo ""
  echo "  3. Paste into the Substack editor"
  echo "     (Skip the metadata block at the top - start from the content)"
  echo ""
  echo "  4. Set canonical URL in post settings:"
  echo "     'This post was originally published elsewhere'"
  echo ""
  echo "     $CANONICAL_URL"
  echo ""
  echo "  5. Preview and publish"
  echo ""
  echo "================================================================"
  echo ""

  # Try to open browser
  if command -v open &> /dev/null; then
    open "https://humainestudio.substack.com/publish/post"
    echo "  Substack editor opened in browser"
  elif command -v xdg-open &> /dev/null; then
    xdg-open "https://humainestudio.substack.com/publish/post" 2>/dev/null &
    echo "  Substack editor opened in browser"
  fi

  # Try to copy canonical URL to clipboard
  if command -v xclip &> /dev/null; then
    echo "$CANONICAL_URL" | xclip -selection clipboard 2>/dev/null && \
      echo "  Canonical URL copied to clipboard!"
  elif command -v pbcopy &> /dev/null; then
    echo "$CANONICAL_URL" | pbcopy 2>/dev/null && \
      echo "  Canonical URL copied to clipboard!"
  fi

  echo ""
  echo "  Tip: Keep this terminal open as your checklist!"
  echo ""
fi
