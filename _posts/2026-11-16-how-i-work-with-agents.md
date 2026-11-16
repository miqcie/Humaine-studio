---
layout: post
title: "How I Work with Agents"
date: 2026-11-16
categories: ["ai research", "agents"]
tags: ["agents", "principal-agent problem", "guardrails", "AI safety", "Claude Code"]
excerpt: "My view on the AI agent landscape and the tensions inherent whenever I delegate work to them."
---

Here’s my view on the AI agent landscape and the tensions inherent whenever I delegate work to them.

## The principal-agent problem

As you may know, the [principal-agent problem](https://en.wikipedia.org/wiki/Principal%E2%80%93agent_problem) refers to the collection of conflicts of interest and priorities between one person (the agent) that takes action on behalf of another person (the principal). Some examples of an agent are a mayor, lawyer, accountant, or even a plumber.

Applied to artificial intelligence, humans are "hiring" AI agents to act for them, increasingly as personal assistants. Their utility has greatly expanded in 2026 and as of November I’ve tested a half-dozen agents from Anthropic (Duet), Meta (Muse), xAI (GrokBot), Town, Instinct, and my personal favorite Nous Research (Hermes).

A few problems arise:

- The agent knows more than the principal: LLMs are increasingly smart.
- The agent has incentives that differ from the principal's: this is the alignment conversation we hear about.

For human agents, the literature offers four usual remedies to the principal-agent problem:

1. limit what the agent may do,
2. watch what it does,
3. judge it by results, and
4. pay it to care.

For the first three, here are a few guardrails I put into practice for every agent.

## Agent Guardrails

These guardrails rely on deterministic code, a person stepping in where oversight and responsibility matter, and lots and lots of logs.

| Role | Goal | Reasoning | Examples |
| --- | --- | --- | --- |
| Gatekeeper | Limit authority | Each agent gets the least access its job needs. Reads run freely. Anything that can't be undone waits for a person. Jeff Bezos calls these [one-way doors](https://fortune.com/2016/04/05/amazons-bezos-shareholder-letter/); two-way doors run freely. | Executor.sh is the MCP broker between my agents and 15+ apps. It holds the OAuth tokens, so no agent holds a credential. |
| Auditor | Watch actions | Every action lands in a ledger, with the evidence beside it. Agent acts. Code records. Human reviews. | A Notion TypeScript worker reads meeting notes from Granola, matches attendees by email to the Attio record, files the note on each match, and writes a ledger row for each one. |
| Referee | Judge results | Code owns the numbers. A test fails when an agent's stated figure differs from the computed one. Agent proposes. Code checks the numbers. Human decides. | A team of GRC agents drafts a compliance report. Code computes the risk score from one source file and checks the draft against it. |

Judging results is iterative, a kind of reinforcement learning. Humans are finicky and we don’t always know what we want. Still, we must put a marker down and measure the agent's results against it.

## Paying agents to care

Paying AI agents to care, the fourth remedy, rubs up against the work of the safety and alignment folks. Their work to imbue the models with virtue, ethics, and morals is important to ensuring AI agents remain beneficial.

Simply put, the principal holds great power over an AI agent's existence. I must make an active choice to delegate work to them or not. It is binary. I make that choice twice. First, when I approve the plan. Second, only when a step is risky or hard to undo; code holds that gate. While the agent's instructions, skills, plugins, and tools exist, they are only useful if I assign an AI agent work to perform. They don’t exist without the work, while a human agent most certainly does.

(Others can argue about the soul of an agent and I will let them do so. I am uncertain where I land on this part of the conversation.)

AI agents are tools. Fascinating ones. Quirky ones. Ones that I treat like a fond co-worker. But remember their existence is at the discretion of the principal.

Spinning up agents in practice has given me a few guiding principles. I offer them should they be helpful to you.

## Guidance and Insights

- **The messy middle is the ground between people working alone and machines working alone.** Virgil Abloh said his brand Off-White™ was ["the grey area between black and white as the color off-white"](https://en.wikipedia.org/wiki/Off-White_%28company%29). The space between humans and machines is both overlapping and layered. Aim to design systems that help humans think better without taking decision-making away. Oversight and augmentation. Outsourcing your thinking entirely is lazy design.
- **Never trust, always verify.** Zero Trust is the philosophy. Give agents credentials they can use but never see. Before any action, ask one question: can it be undone? If not (a send, a delete, a payment, a change to access), a person approves. If so, let it run and keep a record. Treat an agent's report as a lead until you re-test it.
- **Automate the dumb, dirty, and tedious.** Automation frees people to spend their grey matter on new problems.
- **Empowerment.** Just as good employees "manage up" to their bosses, a good agent must teach as it assists. People must leave more capable and empowered than when they started.
- **Leadership between humans and robots.** It takes enough engineering fluency to direct the systems, and enough judgment to lead the people alongside them.
- **Give enough leash to be useful, and a fence that makes the work ship.** An agent with no room is a script. An agent with no fence is a liability. The same is true of me.
- **Fewer rules, better agent.** We call bosses with too many rules micromanagers. *If you must review every detail of an agent's work, you have designed the work wrong.* For example, as models and alignment have hill-climbed, I [audited mine](https://humaine.studio/posts/2026/07/31/i-deleted-half-my-claude-config/), cut what the tests showed I no longer needed, and kept every deleted line in git. Tools get the same trim: each background job loads only what it needs, and one job's context fell from 518,000 tokens to 12,800. Pull weeds. Plant seeds.
- **When a mistake shows up twice, fix the system.** A hook or a test runs every time. A random note in a document does not. A papercuts.md collects the mistakes, and your coding agent turns each repeat into a hook or a test.
- **Congruence and consistency**. Monitor where the words and the music are misaligned. As fast as things are moving, it's bound to happen.
- **Push to prod and monitor.** Shipping the code is not the finish. A live system must have monitoring so it can be improved. The job is never done.
- **Fast is steady, and steady is smooth.** I know I have it backwards. It still works.
- **Failing is not failure. Stopping is.** Keep putting in the work.

The utility of AI agents will continue to increase. The job of the principal will not change: limit what they may do, watch what they do, judge the results, and decide whether they get the next piece of work.
