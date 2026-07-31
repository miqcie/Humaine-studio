---
name: crosspost
description: >-
  Cross-publish a live humaine.studio post to Substack, Medium, X, and
  Instagram — share cards via liftout, platform copy in Chris's voice,
  draft-gated publishing (Playwright drafts for Substack/Medium, API posts for
  X/IG only after Chris approves the copy). Trigger: "/crosspost <post-url>",
  "crosspost this", "mirror to substack/medium", "share this post".
---

# Crosspost pipeline

Input: a LIVE humaine.studio post URL. Never run against a draft — every
platform copy links back to the canonical URL, which must already resolve.

**Draft-gated, always.** Nothing publishes without Chris approving the copy
and the drafts. Playwright creates drafts; Chris clicks Publish. API posts
(X, IG) run only after he approves the exact text.

## 1. Share cards (liftout)

```
/liftout:create <post-url> portrait    # Instagram 4:5
/liftout:create <post-url> landscape   # X / OG
```

Copy the cards into the site so Instagram has a public image URL:
`assets/images/social/<slug>-portrait.png` and `<slug>-landscape.png`.
Commit + PR + merge (cards must be live at humaine.studio before the IG step).

## 2. Platform copy

Draft all four, then show Chris for approval before ANY posting. Voice rules:
plain and direct, parentheses over em dashes, no coined epigrams, no
hashtag-stuffing (see memory: feedback_parens-over-em-dashes,
feedback_no-aphoristic-claude-speak).

- **Substack intro**: 2-3 sentence email hook above the mirrored body.
- **X**: single post, hook + link (a URL-bearing post costs ~$0.22 in API
  credits — one post, not a thread, unless Chris asks).
- **Instagram caption**: 2-4 sentences + "link in bio" phrasing (IG captions
  can't link); note the post URL for Chris's bio link.
- **Medium**: no copy needed (import preserves the article).

## 3. Substack — Playwright draft

1. `mcp__plugin_playwright_playwright__browser_navigate` to
   https://substack.com/home — verify logged in as humainestudio.
2. New post → paste title, intro hook, then the article body (from the live
   page, not the markdown — rendered HTML pastes cleaner).
3. Settings → **set canonical URL to the humaine.studio post**. This is the
   step that must never be skipped; SEO credit depends on it.
4. Save draft. STOP. Tell Chris the draft is ready — he publishes.

## 4. Medium — Playwright import (sets canonical automatically)

1. Navigate to https://medium.com/p/import
2. Paste the post URL, run the import. Medium's importer sets
   `rel=canonical` to the source itself — verify in the imported draft's
   settings that the canonical shows humaine.studio.
3. Fix any mangled figures (check all three images imported).
4. Add up to 5 tags. Save draft. STOP — Chris publishes.

## 5. X — API post (after copy approval)

```
uv run scripts/crosspost/x-post.py "approved post text with URL"
```

One-time setup (documented in the script header): X developer account with
pay-per-use credits; four OAuth 1.0a secrets stored in 1Password item
"X API" in Developer Vault. Never paste keys into the terminal.

## 6. Instagram — Graph API (after copy approval + cards merged)

```
uv run scripts/crosspost/ig-post.py <card-public-url> "approved caption"
```

One-time setup (script header): IG business/creator account linked to a
Facebook page, Meta app with instagram_content_publish, long-lived token in
1Password item "Meta Graph API". If the token or linkage is missing, output
the card path + caption for a 30-second manual post instead of failing.

## 7. Wrap up

- Confirm each platform's final state to Chris in one table (drafted /
  posted / manual-fallback).
- Substack/Medium: remind him both are drafts awaiting his Publish click.
