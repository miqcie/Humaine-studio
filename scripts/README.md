# Scripts

Helper scripts to streamline publishing workflows.

## Quick Reference

```bash
# Format a post for both platforms
python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --output-dir /tmp/formatted

# Publish to Medium (API or manual guide)
./scripts/publish-to-medium.sh _posts/2026-03-02-my-post.md

# Mirror to Substack
./scripts/mirror-to-substack.sh _posts/2026-03-02-my-post.md
```

## format-for-platforms.py

Core formatting engine that converts Jekyll posts into platform-ready content for Substack and Medium. No external dependencies required (uses Python 3 standard library only).

**What it does:**
- Strips Jekyll front matter (layout, date, categories)
- Converts relative links to absolute URLs (`/posts/...` -> `https://humaine.studio/posts/...`)
- Adds platform-specific footers with canonical URL
- For Medium: selects top 3 tags (25 char max), generates API JSON payload
- For Substack: adds email-friendly opening hook from excerpt, subscribe CTA
- Outputs metadata block with title, canonical URL, and publishing instructions

**Usage:**
```bash
# Format for both platforms (print to stdout)
python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md

# Format for one platform
python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --platform medium
python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --platform substack

# Write to files
python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --output-dir /tmp/formatted

# Generate Medium API JSON payload (for automation)
python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --platform medium --api-json --output-dir /tmp/formatted
```

## publish-to-medium.sh

Publishes a Jekyll post to Medium. Supports two modes:

1. **API mode** (if `MEDIUM_INTEGRATION_TOKEN` is set) - Creates a draft directly via Medium's API
2. **Manual mode** (default) - Formats content and guides you through Medium's "Import a Story" feature

**Usage:**
```bash
# Manual mode (no token needed)
./scripts/publish-to-medium.sh _posts/2026-03-02-my-post.md

# API mode (creates draft on Medium)
MEDIUM_INTEGRATION_TOKEN=xxx ./scripts/publish-to-medium.sh _posts/2026-03-02-my-post.md
```

**Notes on Medium API:**
- Medium deprecated their API in March 2023 and stopped issuing new tokens in January 2025
- If you already have a token, it still works
- Check `https://medium.com/me/settings` for "Integration Tokens" at the bottom
- The "Import a Story" fallback works without any token and auto-sets the canonical URL

## mirror-to-substack.sh

Mirrors a Jekyll post to Substack with formatted content and step-by-step guide.

**Two input modes:**
```bash
# From post file (preferred - formats content automatically)
./scripts/mirror-to-substack.sh _posts/2026-03-02-my-post.md

# From URL (legacy - opens browser with checklist)
./scripts/mirror-to-substack.sh "https://humaine.studio/posts/2026/03/02/my-post/"
```

**What it does:**
- Formats post content with email-friendly hook and subscribe CTA
- Extracts canonical URL from post metadata
- Opens Substack editor in browser (if available)
- Copies canonical URL to clipboard (if xclip/pbcopy available)
- Displays step-by-step publishing checklist

## verify-llm-txt.sh

Validates that `llm.txt` is up to date with the current site content.

## Publishing Workflow

### After publishing a new Jekyll post:

```bash
# 1. Push to main (triggers GitHub Pages deploy)
git push origin main

# 2. Wait for site to be live (~2-3 minutes)

# 3. Mirror to Substack
./scripts/mirror-to-substack.sh _posts/YYYY-MM-DD-title.md

# 4. Publish to Medium
./scripts/publish-to-medium.sh _posts/YYYY-MM-DD-title.md
```

### Batch publishing (ADHD-friendly):

```bash
# Format all recent posts at once
for post in _posts/2026-03-02-*.md; do
  python3 scripts/format-for-platforms.py "$post" --output-dir /tmp/batch-publish
done

# Then publish one at a time from the formatted files
```
