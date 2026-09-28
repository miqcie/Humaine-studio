---
layout: post
title: "I Hired Deirdre McCloskey to Edit My Writing (Sort Of)"
categories: ["ai research", "claude code", "writing"]
tags: ["projects", "workflow", "ai", "Deirdre McCloskey", "Claude Code", "agents"]
excerpt: "I turned Deirdre McCloskey's Economical Writing into a Claude Code agent that reviews prose for flab, fog, and AI tics. Then I made her review her own repo. She found problems."
---

I studied English as an undergrad. There were aspirations of politics and/or being a lawyer, and my uncle said that learning to write would always be a good skill to have. Strunk and White was my go-to for simple prose. I distinctly remember a partner at a law firm I worked at taught me a simple construct: tell them what you're going to write, write it, tell them what you just wrote.

Some years later, out of frustration with how AI tries to write, I found [_Economical Writing_](https://press.uchicago.edu/ucp/books/book/chicago/E/bo29562607.html) by Deirdre McCloskey. It's 100-ish pages, funny, and it both ruined my confidence and gave me a way to rebuild it. Once you've read "A Paragraph Should Have a Point" you start noticing most writing doesn't have one. Yes, your writing as well.

Everything I drafted with AI help came out sounding like AI. You know the tells. "It's not just a tool, it's a paradigm shift." The rule-of-three closing. "Moreover." A "delve" if you're unlucky. The writing is cold, inert, and lifeless.

I understand the irony of using a `/skill` in an LLM to help me write. I still think it's a useful exercise. AI is not going anywhere. It is a useful tool. We must learn to use it wisely. So let's use the tool to improve our writing.

Yes, you can grind your own cornmeal. Or you can buy it. It'll be okay.

Here's Deirdre. She's a plugin and a skill. So I did the thing I do now with recurring problems: I made it a Claude Code agent. Her name is deirdre[^1], and she's public.

## What she does

Ask `/deirdre` to review your writing and prose. She reviews your prose the way McCloskey teaches her writing: warm, witty, and intolerant toward flab, fog, and pretentiousness. Two extra rules increase her utility and reduce personal irritation.

1. **Every finding needs a rewrite.** She quotes the offending line, names the rule (McCloskey #25, active verbs — or "LLM tic: not-X-it's-Y"), and hands you a concrete replacement. A rule without a rewrite is a lecture, and she doesn't lecture.

2. **Every cut must improve the clarity, force, or joy of the writing.** The goal is to simplify, but not blunt the impact of your point. A good sentence, no matter its length, that earns its length stays the way it is.

There's a dumb-on-purpose grep script, `llm-lint.sh`, that catches mechanical tics (banned intensifiers, "furthermore," buzzword filler), whatever b.s. Pangram is attempting, and drops them into the response. The grep does the mechanical work; Deirdre is the judge, not regex: rhythm, argument, and opinionated writing is the point.

## Deirdre reviewed herself

I dispatched deirdre to review her own README. This felt like a trap and it was. Verdict: "tighten-then-publish." Findings included:

> "Three pronouns, two referents, one sentence... The information is simple and the sentence is not."

She caught the install section claiming "the skill alone is enough" while the skill referenced a style-guide file the install never copied — "a broken promise in an install section costs more trust than any comma ever will." She caught my LLM-tic list breaking its own rule against redundant restatements. Physician, heal thyself, she said. She's a clever gal.

She also praised what earned it, which is the part of the character I worked hardest to get right. Contemptuous reviewers are easy to build and exhausting to use. McCloskey's actual register — high standards, good cheer, roast the habit and never the human — is what makes me continue to use the tool. I hope you run the review a second time, too.

## Install

Go to [github.com/miqcie/deirdre](https://github.com/miqcie/deirdre). In Claude Code, copy/paste the code below:

```
/plugin marketplace add miqcie/deirdre
/plugin install deirdre@deirdre
```

The plugin is designed as a skill and subagent. The subagent runs the review in its own context, so a long critique stays out of your session. `/plugin update` keeps you up to date as I tinker with improvements.

For other agents that read `SKILL.md` folders (Codex, Hermes, pi), copy or symlink `skills/deirdre/` from the repo. The style guide lives in that folder, so the skill works on its own.

Lastly, buy her book, [_Economical Writing_](https://press.uchicago.edu/ucp/books/book/chicago/E/bo29562607.html).

[^1]: deirdre is a Claude Code plugin and skill inspired by Deirdre McCloskey's _Economical Writing_. The real Professor McCloskey is not involved and is presumably confused or irritated by this distraction.
