# Session Recap: Homepage tagline, CMS call, local Ruby

**Date:** 2026-11-23
**Project:** miqcie/Humaine-studio
**PRs Merged:** #68
**Linear:** HUM-315 (Done)

## What Was Built

- New homepage hero headline: "applied intelligence, human judgment". It replaces "applied ai for human-machine collaboration". It keeps the lowercase display style and the `nowrap` span. Live on humaine.studio (checked with curl after deploy).
- Local Jekyll builds now work. Homebrew `ruby@3.3` (3.3.14) is first on PATH through `~/.zshrc`. `bundle install` and `jekyll build --strict_front_matter` pass.
- Project CLAUDE.md now says Ruby must be 3.x, not 4.

## Key Decisions

| Decision | Rationale |
|---|---|
| No CMS yet | 11 posts in 5 years, 2 since July. Three drafts wait in `_drafts/`: finishing, not publishing, is the bottleneck. Revisit after 2+ posts a month for a quarter, phone editing, or a second editor. Then try a git-backed editor (Pages CMS, Decap) first. |
| Tagline "applied intelligence, human judgment" | Matches the `_config.yml` description ("AI and human judgment") and the hero lede ("keep people in command"). "Humaine" already says human. |
| `ruby@3.3`, not `ruby` (4.0) | `github-pages ~> 228` requires Ruby < 4.0 through commonmarker 0.23. |

## Corrections Applied

- The first edit matched nothing. The session-start snapshot was 6 commits behind `main`, and the brand rollout had moved the tagline into the `<h1>`. Fixed by editing the current markup in the worktree.

## What's Next

- Ruby drift: CI builds on 3.1, local on 3.3 (#60, item 3).
- Optional: `brew uninstall ruby` (4.0) if nothing else uses it.
- Finish one of the three drafts in `_drafts/`.
