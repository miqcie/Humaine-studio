#!/bin/bash
#
# Publish a Jekyll post to Medium via API or guide through Import Story.
#
# Supports two modes:
#   1. API mode (if MEDIUM_INTEGRATION_TOKEN is set) - creates a draft via API
#   2. Manual mode (default) - formats content and guides through Import Story
#
# Usage:
#   ./scripts/publish-to-medium.sh _posts/2026-03-02-my-post.md
#   MEDIUM_INTEGRATION_TOKEN=xxx ./scripts/publish-to-medium.sh _posts/2026-03-02-my-post.md
#
# Environment variables:
#   MEDIUM_INTEGRATION_TOKEN - Your Medium integration token (optional)
#   MEDIUM_USER_ID           - Your Medium user ID (fetched automatically if token set)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Check if post file provided
if [ -z "$1" ]; then
  echo "Error: Please provide the Jekyll post file path"
  echo ""
  echo "Usage:"
  echo "  ./scripts/publish-to-medium.sh _posts/2026-03-02-my-post.md"
  echo ""
  echo "Options:"
  echo "  Set MEDIUM_INTEGRATION_TOKEN env var to use the API"
  echo "  Otherwise, uses Manual Import Story workflow"
  echo ""
  exit 1
fi

POST_FILE="$1"

# Resolve relative path from project root
if [[ ! "$POST_FILE" = /* ]]; then
  POST_FILE="$PROJECT_DIR/$POST_FILE"
fi

if [ ! -f "$POST_FILE" ]; then
  echo "Error: File not found: $POST_FILE"
  exit 1
fi

# Extract post title from front matter
POST_TITLE=$(grep '^title:' "$POST_FILE" | head -1 | sed 's/^title: *//; s/^"//; s/"$//')

echo ""
echo "================================================================"
echo "  Medium Publisher"
echo "================================================================"
echo ""
echo "  Post: $POST_TITLE"
echo ""

# --- API Mode ---
if [ -n "$MEDIUM_INTEGRATION_TOKEN" ]; then
  echo "  Mode: API (integration token detected)"
  echo ""

  # Get user ID if not set
  if [ -z "$MEDIUM_USER_ID" ]; then
    echo "Fetching Medium user ID..."
    USER_RESPONSE=$(curl -s -H "Authorization: Bearer $MEDIUM_INTEGRATION_TOKEN" \
      -H "Content-Type: application/json" \
      "https://api.medium.com/v1/me")

    MEDIUM_USER_ID=$(echo "$USER_RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if 'data' in data:
    print(data['data']['id'])
else:
    print('ERROR: ' + json.dumps(data), file=sys.stderr)
    sys.exit(1)
" 2>&1)

    if [[ "$MEDIUM_USER_ID" == ERROR* ]]; then
      echo "$MEDIUM_USER_ID"
      echo ""
      echo "Could not fetch user ID. Check your MEDIUM_INTEGRATION_TOKEN."
      echo "Falling back to manual mode..."
      echo ""
      MEDIUM_INTEGRATION_TOKEN=""
    else
      echo "User ID: $MEDIUM_USER_ID"
    fi
  fi
fi

if [ -n "$MEDIUM_INTEGRATION_TOKEN" ] && [ -n "$MEDIUM_USER_ID" ]; then
  # Generate API JSON payload
  OUTPUT_DIR=$(mktemp -d)
  python3 "$SCRIPT_DIR/format-for-platforms.py" "$POST_FILE" \
    --platform medium --api-json --output-dir "$OUTPUT_DIR" > /dev/null 2>&1

  BASENAME=$(basename "$POST_FILE" .md)
  API_JSON="$OUTPUT_DIR/${BASENAME}-medium-api.json"

  if [ ! -f "$API_JSON" ]; then
    echo "Error: Could not generate API payload"
    exit 1
  fi

  echo ""
  echo "Creating draft on Medium..."
  echo ""

  RESPONSE=$(curl -s -w "\n%{http_code}" \
    -H "Authorization: Bearer $MEDIUM_INTEGRATION_TOKEN" \
    -H "Content-Type: application/json" \
    -d @"$API_JSON" \
    "https://api.medium.com/v1/users/$MEDIUM_USER_ID/posts")

  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  BODY=$(echo "$RESPONSE" | sed '$d')

  if [ "$HTTP_CODE" = "201" ]; then
    POST_URL=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['url'])")
    echo "Draft created successfully!"
    echo ""
    echo "  URL: $POST_URL"
    echo ""
    echo "  Next steps:"
    echo "    1. Open the URL above"
    echo "    2. Review formatting"
    echo "    3. Verify canonical URL is set"
    echo "    4. Publish when ready"
  else
    echo "API request failed (HTTP $HTTP_CODE)"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
    echo ""
    echo "Falling back to manual mode..."
    MEDIUM_INTEGRATION_TOKEN=""
  fi

  # Clean up temp files
  rm -rf "$OUTPUT_DIR"
fi

# --- Manual Import Story Mode ---
if [ -z "$MEDIUM_INTEGRATION_TOKEN" ]; then
  echo "  Mode: Manual (Import Story)"
  echo ""

  # Generate formatted content
  OUTPUT_DIR=$(mktemp -d)
  python3 "$SCRIPT_DIR/format-for-platforms.py" "$POST_FILE" \
    --platform medium --output-dir "$OUTPUT_DIR" 2>/dev/null

  BASENAME=$(basename "$POST_FILE" .md)
  FORMATTED="$OUTPUT_DIR/${BASENAME}-medium.md"

  # Extract canonical URL from formatted output
  CANONICAL_URL=$(grep "^Canonical URL:" "$FORMATTED" | sed 's/^Canonical URL: *//')
  TAGS=$(grep "^Tags:" "$FORMATTED" | sed 's/^Tags: *//')

  echo ""
  echo "================================================================"
  echo "  Two options for publishing to Medium:"
  echo "================================================================"
  echo ""
  echo "  OPTION A: Import Story (Recommended - easiest)"
  echo "  -----------------------------------------------"
  echo "  1. Go to Medium > Your Profile > Stories"
  echo "  2. Click 'Import a story'"
  echo "  3. Paste this URL:"
  echo ""
  echo "     $CANONICAL_URL"
  echo ""
  echo "  4. Medium auto-imports content + sets canonical URL"
  echo "  5. Add tags: $TAGS"
  echo "  6. Review and publish"
  echo ""
  echo "  OPTION B: Copy formatted content"
  echo "  ---------------------------------"
  echo "  Formatted file saved to:"
  echo "  $FORMATTED"
  echo ""
  echo "  1. Copy content from the file above"
  echo "  2. Create new story on Medium"
  echo "  3. Paste content"
  echo "  4. Set canonical URL in story settings:"
  echo "     $CANONICAL_URL"
  echo "  5. Add tags: $TAGS"
  echo "  6. Publish"
  echo ""
  echo "================================================================"
  echo ""

  # Try to copy canonical URL to clipboard
  if command -v xclip &> /dev/null; then
    echo "$CANONICAL_URL" | xclip -selection clipboard 2>/dev/null && \
      echo "Canonical URL copied to clipboard!"
  elif command -v pbcopy &> /dev/null; then
    echo "$CANONICAL_URL" | pbcopy 2>/dev/null && \
      echo "Canonical URL copied to clipboard!"
  fi
fi

echo ""
