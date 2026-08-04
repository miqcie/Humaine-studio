---
layout: post
title: "I Hired Deirdre McCloskey to Edit My Writing (Sort Of)"
categories: ["ai research", "claude code", "writing"]
tags: ["projects", "workflow", "ai", "Deirdre McCloskey", "Claude Code", "agents"]
excerpt: "I turned Deirdre McCloskey's Economical Writing into a Claude Code agent that reviews prose for flab, fog, and AI tics. Then I made her review her own repo. She found problems."
---

A few years ago someone handed me [*Economical Writing*](https://press.uchicago.edu/ucp/books/book/chicago/E/bo29562607.html) by Deirdre McCloskey. It's 100-ish pages, funny, and it ruined me. Once you've read "A Paragraph Should Have a Point" you start noticing paragraphs that don't have one. Many of them are yours.

Then LLMs happened, and a new problem arrived: everything I drafted with AI help came out sounding like AI. You know the tells. "It's not just a tool, it's a paradigm shift." The rule-of-three closing. "Moreover." A "delve" if you're unlucky. The prose is grammatical, confident, and dead.

So I did the thing I do now with recurring problems: I made it a [Claude Code agent](https://docs.anthropic.com/en/docs/claude-code/overview). Her name is deirdre[^1], and she's public: **[github.com/miqcie/deirdre](https://github.com/miqcie/deirdre)**.

## What she does

You say `/deirdre draft.md` (or just "review this draft") and she reviews your prose the way McCloskey teaches writing: warm, witty, and gently merciless toward flab, fog, and pretension. Two rules make her useful instead of annoying:

1. **Every finding needs a rewrite.** She quotes the offending line, names the rule (McCloskey #25, active verbs — or "LLM tic: not-X-it's-Y"), and hands you a concrete replacement. A rule without a rewrite is a lecture, and she doesn't lecture.
2. **Every cut must buy clarity, force, or joy.** She's not a compression algorithm. A sentence that earns its length keeps it.

There's also a dumb-on-purpose companion: `llm-lint.sh`, a grep script that catches the mechanical tics (banned intensifiers, "furthermore," buzzword filler) and exits 1 so it drops into CI. The grep does the mechanical work; the agent does the judgment a regex can't — rhythm, argument, whether each paragraph has a point.

## The fun part: she reviewed herself

Before promoting the repo, I dispatched deirdre to review her own README. This felt like a trap and it was. Verdict: "tighten-then-publish." Findings included:

> "Three pronouns, two referents, one sentence... The information is simple and the sentence is not."

She caught the install section promising "the skill alone is enough" while the skill referenced a style-guide file the install never copied — "a broken promise in an install section costs more trust than any comma ever will." She caught my LLM-tic list breaking its own rule against redundant restatements. Physician, heal thyself, she said. Literally, that's a quote.

She also praised what earned it, which is the part of the character I worked hardest to get right. Contemptuous reviewers are easy to build and exhausting to use. McCloskey's actual register — high standards, good cheer, roast the habit and never the human — is what makes you run the review a second time.

## Install

```bash
git clone https://github.com/miqcie/deirdre.git
mkdir -p ~/.claude/skills/deirdre
cp deirdre/skills/deirdre/SKILL.md deirdre/STYLE_GUIDE.md ~/.claude/skills/deirdre/
```

That's it — one skill file carries the persona, doctrine, and method. The repo also has the subagent version and a `/deirdre` slash command if you want them.

And buy [the book](https://press.uchicago.edu/ucp/books/book/chicago/E/bo29562607.html). The repo is an homage, not an affiliation. McCloskey said it better in 100 pages than any agent ever will.

[^1]: deirdre is a Claude Code agent inspired by Deirdre McCloskey's *Economical Writing*. The real Professor McCloskey is not involved and is presumably busy writing actual books.
