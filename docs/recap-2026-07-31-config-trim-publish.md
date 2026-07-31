# Session Recap: Config-Trim Experiment, Publication, and Eval Harness

**Date:** 2026-07-29 → 2026-07-31
**Project:** Humaine Studio + claude-config-evals + global Claude Code config
**PRs Merged:** miqcie/Humaine-studio #37, #40; miqcie/claude-config-evals #1

## What Was Built

- **Config trim:** always-on Claude Code context audited (~12K tokens) and cut to ~6K — CLAUDE.md pruned to hard rules + gotchas, 24 skills → 10 (8 CMMC skills → 1 router), bd prime 701→157 words via native PRIME.md override, ponytail/superpowers personas slimmed, PostHog plugin moved to per-repo enablement (Eagle-Ridge, Cmm.dev, Humaine Studio).
- **Eval harness:** 6-task A/B suite with per-cut canaries; verdict non-inferior (18/19 vs 16/18, 10–15% cheaper per run). Extracted to public repo [claude-config-evals](https://github.com/miqcie/claude-config-evals) (MIT, review-hardened: snapshot corruption, XSS, verdict inversion all fixed pre-release).
- **Publication:** [Fewer Rules, Better Agent](https://humaine.studio/posts/2026/07/31/i-deleted-half-my-claude-config/) with 3 generated figures and an interactive results page at `/config-trim-results.html` (generated from results.csv, never hand-edited).
- **Site fix:** `.post-content` CSS gained img max-width + table styling (figures were overflowing the 700px column at 2x natural size; tables rendered unstyled).
- **Crosspost pipeline (deferred):** liftout cards + Playwright drafts (Substack/Medium) + X/IG API scripts, sitting in PR #39 with revive checklist in GH issue #41.

## Key Decisions

| Decision | Rationale |
|---|---|
| Trim kept permanently | Eval non-inferior on every canary; ~45% context reduction; per-rule rollback via backup git repo |
| Eval failures audited before model blamed | 4 of 7 flags were check-script bugs; "audit the judge before the defendant" is now doctrine |
| PostHog plugin per-repo, not global | ~130 skill descriptions only earn their cost in site repos |
| CMMC router stays global | Post-consolidation cost is ~150 words; CMMC questions arise outside repos |
| Medium via import flow, not deprecated API | Import sets rel=canonical automatically |
| Instagram deferred | Weakest channel, token-expiry friction; revisit after 3 manual IG posts |
| Specstory retired | CLI uninstalled; session-sync ritual removed from docs (PR #39) |

## Corrections Applied

- Prose voice: parentheses over em dashes for examples; no coined epigrams ("claude-speak") — both saved as feedback memories.
- Factual: excerpt claimed CLAUDE.md halved (it was session context); beads primer-vs-system contradiction; failure punchline blamed LLMs for a bash bug.

## What's Next

- Substack mirror with canonical URL (CMC-453, manual until pipeline revives)
- Crosspost revival: GH #41 / PR #39 / CMC-454
- Cache-token cost verification ~Aug 14 (bead wpi8)
- Legacy CI red: GH #38 (calculator + religion-map HTML)
- Rotate hardcoded Notion token in settings.local.json (bead r4v7, P1)
