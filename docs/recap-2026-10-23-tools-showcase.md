# Session Recap: Resume out, /tools/ showcase in

**Date:** 2026-10-23
**Project:** miqcie/Humaine-studio (humaine.studio)
**PRs Merged:** #49 (fede0c2), plus this recap PR (footer alignment fix)
**Linear:** HUM-176 (done), HUM-177 to HUM-180 (follow-ups)

## What Was Built

- **Resume removed.** Nav link (pointed at a dead `#resume` anchor), PDF, cover-letter link, and the `.pdf` button CSS that also turned inline footnote PDF links into buttons.
- **/tools/ page.** 18 project cards from 2025-2026 work, in the showcase-writer format: title, status badge (Live, Open source, Private, Archived), lead line, why, named source links, 16:10 screenshot, and the build story folded into `<details>`. A sticky bar filters by group and opens every fold. Live at https://humaine.studio/tools/.
- **Data-driven cards.** `tools.html` loops `_data/showcase.yml` through `_includes/showcase-card.html`. Copy edits never touch markup.
- **Copy round trip.** `scripts/showcase-copy.py export|import|check`: export the cards to one Markdown file, review in Roughdraft, import accepts suggestions and warns about comments. `check` is a round-trip self-test.
- **Evidence sweep.** Four research agents covered 31 repos, session recaps, the memory wiki, Val Town and live sites; four more built per-project fact sheets. Two cards came from Chris's own drafts.
- **CI repaired.** `ubuntu-latest` moved to 26.04 with no Ruby 3.1 build, so CI and the Pages deploy failed before running. Ruby jobs pinned to `ubuntu-24.04`.
- **Footer.** GitHub and Privacy links now sit on one line (this PR).

## Key Decisions

| Decision | Rationale |
|---|---|
| Stay on Jekyll | The page's problems were CSS, not the framework. Move to Astro on Cloudflare when the Ruby toolchain breaks again or more pages need components. |
| Cards in a data file, edited as Markdown | Chris copy-edits prose, not YAML; one include keeps markup consistent. |
| Outcomes over activities | Chris's review: drop pull request, commit and run counts; keep scores, savings and stars. |
| Link every source | Chris's review: "in general, link to sources." All links checked to resolve. |
| Disclosure instead of rewrite | Pangram scored the card copy 0.91 AI. A humanizer pass has not moved Claude-drafted text before. The page says the cards were drafted with Claude and edited by Chris. |
| Roughdraft for local review threads | Chris wants comments to stay local. Claude Docs only for public prose. |
| No family or client details | Spouse reference removed; client names (Nereid, Marlin) and private repos (trust-matter, kids-health-records, interview-coach) kept off the page. |

## Corrections Applied

- `/wrap-up` began on 2025-10-05 as a slash-command shortcut, not on 2026-09-19 (memory updated).
- Chris commits as "Human" as well as "Chris McConnell"; email-filtered commit counts missed his work (memory added).
- Files handed to Chris for editing never go on the iCloud Desktop: the agent gets EDEADLK reading them and the edits did not reach disk (global CLAUDE.md rule added).
- Roughdraft's blocking wait dies at 5 minutes; a background API long-poll with snapshots held for two 20-minute rounds (memory added, install tracked in HUM-177).
- aeo-research val (unmodified template) and claude-grc-agent-demo (a fork) were cut from the page.

## What's Next

- HUM-178 (High): re-check the Optima repo's anonymization now that /tools/ links it.
- HUM-177: install `roughdraft-wait.sh` and update the roughdraft skill.
- HUM-179: confirm the Cal.com to Attio sync is one-way, as the card says.
- HUM-180: Mondrian README links (repo archived).
- GitHub: miqcie/Humaine-studio#50 (specstory rule), miqcie/Humaine-studio#51 (footnote id lint), miqcie/miqcie#3 (profile README link).
