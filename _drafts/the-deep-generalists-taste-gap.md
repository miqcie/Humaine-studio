---
layout: post
title: "The Taste Gap Didn't Close. It Moved."
date: 2026-06-18
categories: ["workflow patterns for human-ai teams", "augmenting knowledge work"]
tags: ["claude code", "taste", "verification", "domain expertise", "agentic coding", "generalists", "human-ai teams", "augmentation"]
excerpt: "I asked Claude to grade me as a developer. The answer inverted the question — and pointed at the one skill agents can't hand you: knowing when the output is wrong."
---

{==1,300-ish days into this AI/LLM moment, I wanted to pause, gaze at my navel, and assess what I've figured out so far using agents to build stuff. Naturally, I asked Geppetto Claude to grade me and pass judgement ;)==}{>>this is too personal. I'm keeping it in, but I think I should remove it.<<}{id="c3" by="user" at="2026-06-22T22:10:45.213Z"}

> {==[This is a follow-up of sorts to a hypothetical conversation I had with Bertram Gilfoyle last year about what makes a 'developer'](https://humaine.studio/posts/2025/08/18/gilfoyle/)==}{>>this is too personal. I'm keeping it in, but I think I should remove it.<<}{id="c3" by="user" at="2026-06-22T22:10:45.213Z"}

{==Maybe I could _actually_ code now and that the English degree and the self-taught nights has made me a [real boy, i mean developer](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnMydTgybmVhMzB3YjRrYWNiOGlyZnJjaWs4NjV5eDJvZDQ2ZG1qdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5BkTsCPkXcMNE5vBfI/giphy.gif) or just a convincing fascimile of one.==}{>>this is too personal. I'm keeping it in, but I think I should remove it.<<}{id="c3" by="user" at="2026-06-22T22:10:45.213Z"}

Expertise is a tricky subject nowadays and its definition is slippery.

An expert is "a person who has comprehensive and authoritative knowledge of or skill in a particular area" (NOAD)

Deep skill, like coding proficiency, does not have the same predictive powers of expertise as they once did. Technical skills do little to determine how well someone is able to develop, use, and manage agents.

Recent research suggests that domain knowledge, which may not be readily captured by training data, is a better predictor on using agents capablly.

An accountant who knows the daily rhythms of reconciliation rules for their industry but has never written Python will run circles around a senior engineer touching a new language for the first time. The senior engineer, in that moment, is the novice.
## What the research actually found
Two recent studies from Anthropic.

The first ([what makes Claude Code users effective](https://www.anthropic.com/research/claude-code-expertise)) looked at what separates experts from novices using the tool. Domain expertise won, not coding background. People decide _what_ to build — they own roughly seventy percent of those calls — and the agent decides _how_, owning about eighty percent of the execution. Experts trigger more than twice the agent actions per prompt than novices do. They drive harder because they know where they're going.

The second study ([how AI assistance affects coding skill](https://www.anthropic.com/research/AI-assistance-coding-skills)) carried a warning. Developers who leaned on AI scored about seventeen percent lower on later assessments — close to two letter grades — than those who worked unaided. The largest drop showed up in debugging: knowing when code is wrong and why it fails. The skill most at risk of atrophy is the exact skill you need to supervise the machine.

People who asked the agent to explain its reasoning, who posed conceptual questions, who debugged the errors themselves instead of pasting them back for a fix — they held their skill or gained it. The researchers put it plainly: **cognitive effort, even getting painfully stuck, builds mastery**. The tool can teach you or rot you, and your habits pick which.

{==[Outsourcing cognition](https://pmc.ncbi.nlm.nih.gov/articles/PMC12714973/)==}{>>need to read this and talk about it more. Sometimes mowing your own lawn is better than hiring someone.<<}{id="c1" by="user" at="2026-06-18T15:46:15.287Z"}

This is where the deep generalist wins. Curiosity gets you to a domain. Then you go deep, until you've earned the taste — the trained sense for what good looks like in compliance, or radio, or diabetes hardware. The checks come last, and they prove the taste is real instead of imagined. Do all three and you build things a narrow specialist and a pure generalist both miss: the specialist won't range wide enough, the generalist won't go deep enough to know when the output lies.
## The gap Ira Glass named
{==Ira Glass has a notable quote, from a 2007 [Gothamist](https://gothamist.com/arts-entertainment/ira-glass-this-american-life) interview, about taste. It came to mind when I was thinking about this missive as well as the twitter cognosetti blabbing about how important taste is to differentiated products.==}{>>this is terribly overwritten, but the big words were what were in my head.<<}{id="c2" by="user" at="2026-06-18T16:07:59.983Z"}

> "Nobody tells this to people who are beginners, I wish someone told me. All of us who do creative work, we get into it because we have good taste. But there is this gap. For the first couple years you make stuff, it's just not that good... But your taste, the thing that got you into the game, is still killer. And your taste is why your work disappoints you."

Ira's prescription was volume. Do a huge amount of work, finish one thing a week, and the gap between your taste and your output will close. Yeah. it's the boring shit. You put in the work and you gradually improve.

The advice still holds. Us humans used to be a bottleneck to production. Agents can ship faster than we can read what happened, but this also

You had taste on day one — you could hear a bad sentence, spot a clumsy interface, smell a wrong number. What you lacked was the thousands of reps to make your hands match your ear.

Agents collapse that bottleneck. I describe a feature and Claude writes it across nine files, runs the tests, and commits. The reps I used to grind out by hand now arrive in seconds. So the production gap — the one Glass told us to close with volume — barely exists for me anymore.

A different gap opened in its place. The gap between output that _looks_ right and output I've _proven_ right. That gap is now the whole job. Call it what it is: taste, relocated. Taste used to mean recognizing good work. Now it means catching the plausible-but-wrong thing that an agent hands you with total confidence.
## How my work has adapted
My workflow patterns are mostly building machinery to be skeptical of the machine and it's occassional stochastic outputs.

When I had Claude plan and code some recent changes to a compliance product I'm working on, I send `/gilfoyle`, whose whole job is to tell me how/why Claude and I are wrong. It's a humorous and educational feedback loop.

For more substantial work. I run several reviewers at once, each with a narrow brief: one hunts structural problems, one checks test coverage, one looks only for swallowed errors, one reads the comments against the actual code. On one recent change the four of them surfaced four distinct defects, and no single reviewer would have caught another's. One agent has blind spots. Four with different orders see more of the board.

I use Steve Yegge's beads to keep a shared memory across sessions — a command-line log of decisions, so the agent and I avoid rehashing.

The most consequential habit is also a dull one.

I am consistently asking Claude to find ways to be things more simple, more verifiable, and "immutable" when they need to be. For those generalists out there, immutable just means that it can't be changed. It's a big deal for code wranglers.

Agent self-reports are not evidence. But I've found that asking for the source truth behind claims helps a lot.

It's my own paranoia about skillfulness transferred to my agent harness.
## Hill Climbing
I haven't arrive at those checks by reading a manual, because it doesn't exist. I earned each scar one by trusting blindly. The procedures are the protocols to prevent the next scar.

A migration agent once told me it had moved everything — "all records migrated." I almost believed it. Then I dumped the raw rows and ran my own count: the source held 220, and the agent's own reports disagreed with themselves about whether the copy had 220 or 210. One off-hand "done" nearly cost me real data. The lesson became a rule: copy, don't move; keep the source until a reconciliation script I wrote — not the agent's word — proves the copy matches by content, row for row.

I burned a string of sessions on a website that wouldn't update. I'd push code, see green, and assume the change was live. It wasn't. The hosting project took direct uploads, so a git push deployed nothing at all. The fix was humbling in its simplicity: a push is not a deploy. Now I `curl` the live URL and read the changed bytes back before I believe anything shipped.

I have a clock that shows my blood sugar, built on an ESP32 microcontroller. Continuous integration — the automated build that runs on every change, CI for short — went green for weeks while the firmware failed on the actual chip. A fake build environment can't surface a bug that only the real silicon has. So I flash the device and watch it boot before I push, every time.

Even my agents taught me this by failing. I once wired up an executor agent to escalate hard problems to a smarter advisor agent, and it couldn't — a dispatched subagent doesn't automatically get the tool to dispatch others. The escalation I'd assumed simply didn't exist until I designed it on purpose.

Every one of those checks exists because I trusted output that looked right and got burned. The checks are self-referential at their core. I couldn't have written the verification rules in advance, because I didn't yet have the taste to know what deserved suspicion. The failures grew the taste. The taste became the checks.
## For the generalist, and for the people studying us
If you know a domain in your bones and you've talked yourself out of building because you're "not a real engineer" — stop apologizing. Your domain depth is the scarce input now. The agent supplies the syntax you were missing. Your job is to want the right thing, then to prove the machine actually delivered it. Both halves matter. Domain knowledge without checks ships confident nonsense. Checks without domain knowledge can't tell you what to check for.

And to the researchers measuring how these skills form: the old rubric grades the wrong thing. Counting whether someone can write a sort from memory tells you less every month. The skills that compound are domain modeling, verification judgment, and the orchestration sense to direct several agents and catch their disagreements. Your own finding — that the same tool builds skill in active hands and erodes it in passive ones — means the variable worth measuring isn't _whether_ people use AI. It's _how_. Measure the habits, not the headcount.
## Fight your way through
Glass said you close the gap by doing a huge volume of work, and that you've just gotta fight your way through. The advice survives the agent era intact. The work hasn't vanished — it changed shape. The volume I put in now isn't typing. It's judgment: directing the work, then trying to prove it wrong, over and over, until catching the plausible-but-broken answer becomes reflex.

That reflex is the new taste, and you grow it the way Glass said you grow the old one. You do a lot of it. You get painfully stuck on purpose. You fight your way through.
