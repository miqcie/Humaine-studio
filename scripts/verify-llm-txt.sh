#!/bin/bash
# Verification script for llm.txt maintenance and accessibility

set -e

echo "🔍 Verifying llm.txt..."
echo ""

# Check if llm.txt exists
if [ ! -f "llm.txt" ]; then
  echo "❌ llm.txt not found at repository root"
  exit 1
fi

echo "✅ llm.txt exists at repository root"

# Count blog posts in _posts/
if [ -d "_posts" ]; then
  POST_COUNT=$(ls -1 _posts/*.md 2>/dev/null | wc -l | tr -d ' ')
  echo "📝 Blog posts in _posts/: $POST_COUNT"
else
  POST_COUNT=0
  echo "⚠️  No _posts/ directory found"
fi

# Check blog post count in llm.txt
LLMTXT_SECTION=$(grep -A 20 "### Blog Posts" llm.txt || echo "")
if echo "$LLMTXT_SECTION" | grep -q "published)"; then
  LLMTXT_COUNT=$(echo "$LLMTXT_SECTION" | grep "published)" | sed 's/[^0-9]*//g')
  echo "📄 Blog posts in llm.txt: $LLMTXT_COUNT"

  if [ "$POST_COUNT" != "$LLMTXT_COUNT" ]; then
    echo "⚠️  MISMATCH: llm.txt shows $LLMTXT_COUNT posts but _posts/ has $POST_COUNT"
    echo "   → Update the 'Blog Posts' section in llm.txt"
  else
    echo "✅ Blog post count matches"
  fi
else
  echo "⚠️  Could not find blog post count in llm.txt"
fi

# Check last updated date
LAST_UPDATED=$(grep "Last Updated" llm.txt | head -1 || echo "Not found")
echo "📅 $LAST_UPDATED"

TODAY=$(date +%Y-%m-%d)
if ! echo "$LAST_UPDATED" | grep -q "$TODAY"; then
  DAYS_OLD=$(( ($(date +%s) - $(date -d "$(echo $LAST_UPDATED | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')" +%s)) / 86400 ))
  if [ $DAYS_OLD -gt 30 ]; then
    echo "⚠️  llm.txt is $DAYS_OLD days old - consider updating if content changed"
  fi
fi

echo ""
echo "🌐 Testing local accessibility..."

# Check _config.yml has llm.txt in include directive
if grep -q "llm.txt" _config.yml; then
  echo "✅ llm.txt is listed in _config.yml include directive"
else
  echo "❌ llm.txt NOT in _config.yml include directive"
  echo "   → Add 'llm.txt' to the 'include:' section in _config.yml"
  exit 1
fi

# Check if Jekyll can build
if command -v bundle &> /dev/null && bundle exec jekyll --version &> /dev/null; then
  echo "Building site with Jekyll..."
  if bundle exec jekyll build --quiet 2>&1 | grep -q "error"; then
    echo "❌ Jekyll build failed"
    exit 1
  fi

  if [ -f "_site/llm.txt" ]; then
    echo "✅ llm.txt exists in _site/ after build"

    # Check file size
    SIZE=$(wc -c < _site/llm.txt)
    if [ $SIZE -lt 100 ]; then
      echo "⚠️  llm.txt seems very small ($SIZE bytes) - might be incomplete"
    else
      echo "✅ File size: $SIZE bytes"
    fi
  else
    echo "❌ llm.txt NOT found in _site/ after build"
    echo "   → Verify _config.yml include directive is correct"
    exit 1
  fi
else
  echo "⚠️  Jekyll not available, skipping build test"
  echo "   → Will be tested during GitHub Pages deployment"
fi

echo ""
echo "📋 Quick Checklist:"
echo "  [ ] Blog post count matches _posts/ directory"
echo "  [ ] Last Updated date is current"
echo "  [ ] File builds to _site/llm.txt"
echo "  [ ] After deploy: curl https://humaine.studio/llm.txt"
echo "  [ ] Test with LLM: 'Read humaine.studio/llm.txt and summarize'"
echo ""
echo "✅ Local verification complete!"
