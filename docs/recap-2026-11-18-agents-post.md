# Session Recap: "How I Work with Agents" published, link-check fixed

**Date:** 2026-11-16 to 2026-11-18
**Project:** miqcie/Humaine-studio (humaine.studio)
**PRs Merged:** #54 (a8d3ee1), #55 (8be904f)

## What Was Built

- **#54:** published `_posts/2026-11-16-how-i-work-with-agents.md` from Chris's draft. The text is unchanged. Mechanical fixes only: the title and byline moved to front matter, stray `&#32;` entities were removed, and three broken bold/italic markers were closed. llm.txt lists 13 posts. Live at https://humaine.studio/posts/2026/11/16/how-i-work-with-agents/.
- **#55:** link-check no longer fails on new-post PRs. On PR runs only, a step adds `'^https://humaine[.]studio/'` to the exclude list in `lychee.toml`. Push-to-main and weekly runs still check humaine.studio links.

## Key Decisions

| Decision | Rationale |
| --- | --- |
| Merge #54 with link-check red | The only error was the post's own canonical URL, which 404s until deploy. The re-run after deploy passed. |
| PR runs skip humaine.studio links | Every new post would otherwise show a red check. A check that is always red stops meaning anything. |
| Edit `lychee.toml` in CI, not `--exclude` | A CLI `--exclude` replaces the config's exclude list. The font CDN and PostHog opt-out exclusions came back as failures. |

## Corrections Applied

- First fix used `--exclude` on the command line. The PR run showed it dropped the config exclusions; replaced with the `lychee.toml` edit step in the same PR.

## What's Next

- miqcie/Humaine-studio#56: check humaine.studio links against the PR build (lychee `remap`) instead of skipping them.
- HUM-270: mirror the post to Substack with the canonical URL.
