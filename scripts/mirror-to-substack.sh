#!/bin/bash
#
# Helper script for mirroring Jekyll posts to Substack
# Reduces friction by opening the necessary URLs and providing reminders
#
# Usage: ./scripts/mirror-to-substack.sh "https://humaine.studio/posts/2025/11/25/post-title/"
#

set -e

# Check if URL provided
if [ -z "$1" ]; then
  echo "❌ Error: Please provide the post URL"
  echo ""
  echo "Usage:"
  echo "  ./scripts/mirror-to-substack.sh \"https://humaine.studio/posts/2025/11/25/post-title/\""
  echo ""
  exit 1
fi

POST_URL="$1"

# Extract post title from URL for display
POST_TITLE=$(echo "$POST_URL" | sed 's/.*\/\([^/]*\)\/*$/\1/' | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📧  Substack Mirroring Helper"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Post to mirror: $POST_TITLE"
echo "Source URL: $POST_URL"
echo ""
echo "Opening in your browser:"
echo "  1. Your published Jekyll post (to copy content)"
echo "  2. Substack editor (to paste and publish)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Open both URLs
open "$POST_URL"
sleep 1
open "https://humainestudio.substack.com/publish/post"

echo "✅ URLs opened!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝  Checklist:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  [ ] Copy content from Jekyll post"
echo "  [ ] Paste into Substack editor"
echo "  [ ] Add email-friendly opening hook"
echo "  [ ] Add footer: 'Originally published at [URL]'"
echo "  [ ] Add call-to-action (subscribe, share, etc.)"
echo "  [ ] Set canonical URL in post settings:"
echo "      ☑️  'This post was originally published elsewhere'"
echo "      📍 Canonical URL: $POST_URL"
echo "  [ ] Preview post"
echo "  [ ] Publish or schedule"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Tip: Keep this terminal open as your checklist!"
echo ""
echo "Canonical URL (copy this):"
echo "$POST_URL"
echo ""
