# Scripts

Helper scripts for cross-posting Jekyll posts to Substack and Medium.

## Quick Reference

```bash
# Format a post for both platforms
python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --output-dir /tmp/formatted

# Publish to Medium (Import Story guide)
./scripts/publish-to-medium.sh _posts/2026-03-02-my-post.md

# Mirror to Substack
./scripts/mirror-to-substack.sh _posts/2026-03-02-my-post.md
```

## format-for-platforms.py

Core formatter. Converts Jekyll posts into platform-ready content. No external dependencies (Python 3 stdlib only).

- Strips Jekyll front matter
- Converts relative links to absolute URLs
- Medium: adds title heading, selects top 3 tags, "Originally published at" footer
- Substack: adds email hook from excerpt, subscribe CTA footer
- Outputs metadata block with canonical URL and publishing instructions

```bash
python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md                          # both platforms, stdout
python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --platform medium         # medium only
python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --output-dir /tmp/out     # write to files
```

## publish-to-medium.sh

Guides you through Medium's "Import a Story" feature — the only reliable publishing method since Medium deprecated their API (March 2023) and stopped issuing tokens (January 2025).

```bash
./scripts/publish-to-medium.sh _posts/2026-03-02-my-post.md
```

Import Story auto-sets the canonical URL and backdates the post. No token needed.

## Quick Reference

Formats and guides Substack publishing. Accepts a post file or URL.

```bash
./scripts/mirror-to-substack.sh _posts/2026-03-02-my-post.md                                   # file (preferred)
./scripts/mirror-to-substack.sh "https://humaine.studio/security/compliance/2026/03/02/post/"   # URL (legacy)
```

## verify-llm-txt.sh

Validates that `llm.txt` is up to date with current site content.
