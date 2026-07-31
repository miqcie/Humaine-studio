---
layout: post
title: "Fewer Rules, Better Agent: Testing Anthropic's Context Advice on My Own Setup"
date: 2026-07-31
categories: [ai, tooling]
tags: [claude-code, context-engineering, evals, ai-tooling, llm-ops]
excerpt: "Anthropic says their newest models perform better with fewer constraints (they cut 80% of Claude Code's own system prompt). I ran their advice on my own config, tested before/after on a 6-task eval, and cut my session context in half."
---

Thariq Shihipar at Anthropic recently published [The New Rules of Context Engineering](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models). The main point is newer Claude models require fewer constraints. The system prompts, hooks, and skills files started to conflict and add cruft, with Claude ignoring its own rules. As a result, they removed over 80% of Claude Code's own system prompt and measured no loss in performance. The logic was elegant: rules to prevent old-model failures added unnecessary context on every request, putting constraints on a model that no longer needed them.

I wanted to verify this with my own setup. Claude read the blog, reviewed my CLAUDE.md rules, my custom skills, plugins, and my task triage setup. It's a year+ of accumulated thinking and hacks. While there was a lot of noise on social media about the performance of the 5-class models, this felt like a good time to revisit my setup.

Claude set up the experiment in 3 parts:

1. Audit the session context at startup
2. Edit customizations (skills, plugins, hooks), without affecting performance. Can we make [ponytail](https://github.com/DietrichGebert/ponytail) an even better lazy dev?
3. Run before/after evals to see if costs were lowered while performance remained the same.

## Audit

My current session context is around 12,000 tokens. Reviewing it showed how generic parts of it were, like "be autonomous" and "fix root causes". The audit also found my config arguing with itself. For example, I use [beads](https://github.com/steveyegge/beads) for task-memory across repos. Beads said "do NOT use MEMORY.md", but my CLAUDE.md would override it because I still wanted other non-task memories to be saved in the harness. Maybe Steve Yegge is cringing (if he ever reads this), but don’t yuck my yum, ok?

I also have [ponytail](https://github.com/DietrichGebert/ponytail) that injects a "lazy senior developer" persona to fight over-engineering, which fits into my preference to have agents write like the economist Deirdre McCloskey: direct, clear, concise, and data/evidence-based. But the ponytail ruleset mainlined 1,100-words to every subagent. A little overkill on grep read-only file searches. 

Audit findings were thrown into 3 buckets: is it a _hard rule_ that must be followed, a _gotcha rule_ the model can't discover (like "pushes to this repo don't deploy"), or is it a _generic behavior rule_ that newer models no longer need help with? We focused on removing generic behavior rules as newer models have become more capable.

## Trim

![Always-on context per component, before and after the trim](/assets/images/config-trim/fig-trim.png)

Skills were combined, removed, or shrunk (24 skills → 10). 

Claude also recommended that the compliance skills I use with my GRC startup eagleridge.io be merged into a router that loads the skills as needed.

I also fixed a lazy mistake where the [PostHog plugin](https://github.com/PostHog/ai-plugin) was global instead of only available on the repos I actually needed it on.

Ponytail was trimmed to 250 words from 1,100 by keeping specific conventions and removing some of the overly-persuasive "scaffolding". The beads primer had a native override file that I didn't use. This shrunk beads from 700 words to 157. Hook-based rules shrank to one line with a pointer to the file.

The idiosyncratic stuff that made my setup personal was saved. Beads itself, the task-memory system I run my projects on, was untouched (only its primer got shorter).

The result was a 50% net-reduction (~12K to ~6K) in session context.

## Evals

I didn't want to [lobotomize](https://x.com/DaniBeckman/status/1779306426076397970) my Claude setup or start from scratch. I'm still skeptical about trusting LLM outputs blind, no matter how bafflingly brilliant they can be. I prefer to have Claude "prove" its recommendations instead of "just trust me bro."

Claude built six tasks to generate evidence and compare before/after performance. They were each an objective check and mapped to one specific cut in the session context. The tasks were canaries in a coal mine. A failure tied back to the specific rule modified. This simplified the process to revert changes and restore the original rule if needed.

For example, would cutting `ponytail` cause Claude to add dependencies instead of a stdlib one-liner? Would trimming the skill-enforcement block prevent domain-specific skills from firing? Would a cut to the `git-workflow` mess up a feature branch? Both configs ran each task three times in a headless set up. The costs and outputs were logged to a CSV. The full run-level data is in the [results dashboard](/config-trim-results.html) for you data-obsessives to dive into.

## Results

|     | Old config | Trimmed config |
| --- | --- | --- |
| Task pass rate | 16/18 | 18/19* |
| Cost per run | ~$0.88–1.41 | ~$0.77–1.06 (10–15% lower) |

<small>*The trimmed config included an extra smoke-test run.</small>

The trimmed config did no harm. It continued to pass everything the old config passed. Costs came in lower on five of six tasks:

![Median cost per run by task, old config vs trimmed](/assets/images/config-trim/fig-cost.png)

Both configs struggled running some headless git tasks, which would matter if I was running API calls in a production environment.

## What failed: my tests

Claude flagged a few runs due to poor experiment design, not model failure.

![Failure anatomy: 4 check-script bugs vs 3 real headless failures](/assets/images/config-trim/fig-anat.png)

Four were bugs in the check scripts. The model did a textbook branch → commit → merge workflow; my check flagged it because the final branch was `main`. The model wrote "expressly ineligible" (a correct compliance answer) and my grep only knew the phrase "not eligible." One check handed a passing grade to a run that never executed, because the untouched fixture happened to satisfy it. Shell scripts!!!!

The three real failures were tied to one behavior mentioned above: headless one-shot runs sometimes commit to `main` instead of the feature-branching I require. Both configs did it. The fix is a hook, or a line in the automation's own prompt, not more config detail.

**When an eval fails, audit the judge before the defendant.** 

## The compliance angle

My day job is [cybersecurity compliance consulting](https://eagleridge.io), so this felt like me applying that mindset to auditing developer workflows. Just like that junk drawer in your kitchen, controls can accumulate because there's less friction to add one more thing than to pause and see what needs to be removed. People I worked with have heard me talking about "pulling weeds and planting seeds" ad nauseam over the years. It's the same concept. Sometimes you just gotta take a fresh view against the current state of the world to see if things still make sense. Not rely on vibes or blindly trust these rapidly improving agents to understand what's in your brainspace.

Applying this back to compliance, config files for AI agents are control registers. They require the same fix: inventory, classify against current capability, cut with a rollback path, verify with tests. My rollback is a git repo holding every deleted line; the evals re-run in minutes when the next model generation ships.

I was pleased that the advice Anthropic gave improved my setup and that it aligned with my current process to "measure, cut, and verify."

## Try it yourself

If your CLAUDE.md is over ~500 words, an audit will probably surprise you. Here's how you can run it yourself:

1. **Audit:** ask Claude to inventory everything injected at session start (rules file, skill descriptions, plugin hooks, MCP instructions) with a rough token count per component.
2. **Sort:** for each line, ask the 3-bucket question above (hard rule, gotcha, or generic behavior). Snapshot everything to git before touching anything.
3. **Trim:** cut the generic category, look for native override mechanisms before rewiring anything, and let hooks replace prose where a hook already enforces the rule.
4. **Verify:** write one small headless task per cut with a pass/fail check, run it against both configs, and audit any failure's check script before blaming the model.

The harness (snapshot/restore safety net, eval runner, dashboard, and example canaries) is open source: [claude-config-evals](https://github.com/miqcie/claude-config-evals). Clone it, open Claude Code inside it, and your own Claude will personalize the canaries to your setup.
