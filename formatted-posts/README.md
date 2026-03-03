# Formatted Posts for Cross-Platform Publishing

This directory contains blog posts formatted for Substack and Medium distribution.

## Structure

```
formatted-posts/
├── substack/          # Substack-formatted versions
│   ├── security-poverty-line.md
│   ├── evidence-first-vs-detection-only-security.md
│   └── experiments-building-grc-tool-weekend.md
├── medium/            # Medium-formatted versions
│   ├── security-poverty-line.md
│   ├── evidence-first-vs-detection-only-security.md
│   └── experiments-building-grc-tool-weekend.md
└── README.md          # This file
```

## Platform Differences

### Substack Format
- Email-friendly opening hook (italic teaser before the horizontal rule)
- Inline links with full URLs to humaine.studio
- "Originally published at" footer with canonical URL
- Canonical URL reminder at bottom for post settings
- No code-heavy formatting (email clients have limited rendering)

### Medium Format
- Subtitle as H2 below the title (Medium's subtitle field)
- Clean paragraph formatting (Medium renders markdown well)
- Import instructions at bottom with canonical URL
- Suggested tags and publications for discoverability
- Code blocks preserved (Medium supports syntax highlighting)

## Publishing Workflow

### Substack (humainestudio.substack.com)
1. Copy content from `substack/` version
2. Paste into Substack editor at https://humainestudio.substack.com/publish/post
3. Set canonical URL in post settings
4. Preview and publish

### Medium (@humaine.studio)
1. Use Medium's "Import a story" with the canonical URL, OR
2. Copy content from `medium/` version and paste into Medium editor
3. Set canonical link in Story Settings
4. Add suggested tags
5. Submit to relevant publications

## Canonical URLs (Critical for SEO)
Always set the canonical URL to the original humaine.studio post:
- Security Poverty Line: https://humaine.studio/posts/2026/03/02/security-poverty-line/
- Evidence-First Security: https://humaine.studio/posts/2026/03/02/evidence-first-vs-detection-only-security/
- GRC Tool Weekend: https://humaine.studio/posts/2026/03/02/experiments-building-grc-tool-weekend/
