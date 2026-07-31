---
layout: post
title: "Fewer Rules, Better Agent: Testing Anthropic's Context Advice on My Own Setup"
date: 2026-07-31
categories: [ai, tooling]
tags: [claude-code, context-engineering, evals, ai-tooling, llm-ops]
excerpt: "Anthropic says their newest models perform better with fewer constraints (they cut 80% of Claude Code's own system prompt). I tested the claim on my own config: audited 12,000 tokens of accumulated rules, deleted half, and ran both versions through a six-task eval. Results inside."
---

Thariq Shihipar at Anthropic recently published [The New Rules of Context Engineering](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models). The main point is newer Claude models require fewer constraints. The system prompts, hooks, and skills files started to conflict and add cruft, with Claude ignoring its own rules. As a result, they removed over 80% of Claude Code's own system prompt and measured no loss in performance. The logic was elegant: rules to prevent old-model failures added unnecessary context on every request, putting constraints on a model that no longer needed them.

I wanted to verify this with my own setup, and had Claude read the blog, then review my CLAUDE.md rules, all of my custom skills, plugins, and my task triage setup. It's a year plus of accumulated stuff. This felt like a great time to revisit my setup.

Using Claude, the experiment ran 3 parts:

1. Audit the session start and inventory everything injected into context before I type a word
2. Trim skills, plugins (ie [ponytail](https://github.com/DietrichGebert/ponytail) and others), and my rules file to see where we could reduce tokens without affecting performance
3. Run evals on the before/after states to see if performance held, and if costs were lowered

## The audit

Claude spun up an agent to inventory the system context whenever I spun up a new session. It was about 12,000 tokens. I was surprised how generic I was in my setup. About 40% of my rules file was generic behavior (ie. "be autonomous," "fix root causes"). The audit also found my config had it arguing with itself. For example: the session primer for my task-memory system (Steve Yegge's [beads](https://github.com/steveyegge/beads)) said "do NOT use MEMORY.md" while CLAUDE.md would override it. And [ponytail](https://github.com/DietrichGebert/ponytail), a plugin that injects a "lazy senior developer" persona to fight over-engineering, injected its full 1,100-word ruleset on every subagent. A five-subagent session wasted ~9,000 tokens doing read-only file searches.

We sorted things into 3 buckets: is it a _hard rule_ that must be followed, a _gotcha_ rule the model can't discover (like "pushes to this repo don't deploy"), or is it a _generic behavior_ rule that newer models don't need help with? The last one was the rule that would be removed.

## The trim

![Always-on context per component, before and after the trim](/assets/images/config-trim/fig-trim.png)

Component by component: skills shrank through consolidation (24 skills → 10, eight compliance skills merged into a router that loaded phase files on demand) and making the [PostHog plugin](https://github.com/PostHog/ai-plugin) only be available on specific repos, not a global setting. Ponytail was reduced to 250 words, instead of 1,100, by keeping specific conventions and removing some of the persuasion scaffolding. The beads primer had a native override file that I didn't use: 700 words → 157. Rules enforced by hooks shrank to one line each pointing to the file.

I still kept the idiosyncratic stuff that made my setup personal, and the memory system that I run my projects on.

The net is a 50% reduction (~12K to ~6K).

## The eval

It would have been easy to use an axe instead of a scalpel to trim the config. But I didn't want to [lobotomize](https://x.com/DaniBeckman/status/1779306426076397970) Claude. And I'm still skeptical about trusting LLM output blind, no matter how bafflingly brilliant it can be. I needed evidence, not just "trust me bro."

Claude built six fixed tasks, each with an objective check and mapped to one specific cut. These were like canaries in a coal mine. Each task was an early-warning signal for one deletion, so any failures were tied back to the specific rule we modified. This simplified the process to revert changes and restore the original rule. For example, would cutting the anti-over-engineering persona lead Claude to add dependencies instead of a stdlib one-liner? Would cutting the skill-enforcement block stop domain skills from firing? Would cutting the git-workflow prose stop work from landing on a feature branch? Both configs ran every task three times, headless, costs and outcomes logged to CSV. Full run-level data is in the [results dashboard](/config-trim-results.html), where every row expands to the exact prompt, the check, and each run's actual output.

## Results

|     | Old config | Trimmed config |
| --- | --- | --- |
| Task pass rate | 16/18 | 18/19* |
| Cost per run | ~$0.88–1.41 | ~$0.77–1.06 (10–15% lower) |

<small>*The trimmed arm includes one extra smoke-test run.</small>

The trimmed config passed everything the old config passed, at lower cost on five of six tasks:

![Median cost per run by task, old config vs trimmed](/assets/images/config-trim/fig-cost.png)

The only task either config struggled with was running some headless git tasks (which would matter if I was running API calls), and the old config, with all its workflow prose loaded, did _worse_ (1/3 vs 2/3). The rules I'd written to enforce that behavior weren't enforcing it.

## What failed: my tests

A few runs were flagged due to poor experiment design, not model failure.

![Failure anatomy: 4 check-script bugs vs 3 real headless failures](/assets/images/config-trim/fig-anat.png)

Four were bugs in my own check scripts. The model did a textbook branch → commit → merge workflow; my check flagged it because the final branch was `main`. The model wrote "expressly ineligible" (a correct compliance answer) and my grep only knew the phrase "not eligible." One check even passed on a run that never executed, because the untouched fixture happened to satisfy it.

The three real failures were all one behavior: headless one-shot runs sometimes commit to `main` instead of branching. Both configs did it. That's a property of headless mode, and the fix is a hook or a line in the automation's prompt, not more config prose.

**When an eval fails, audit the judge before the defendant.** LLM outputs are diverse; brittle checks convert correct behavior into fake regressions, and fake regressions will talk you into keeping config you don't need.

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
