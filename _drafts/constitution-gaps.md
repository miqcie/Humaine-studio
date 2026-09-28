# The Gaps in Claude's Constitution: A Humanities and Organizational Behavior Perspective

**Working Draft — Chris McConnell**

---

## The Core Argument

Claude's constitution is a philosophy document built by people trained in analytic philosophy and machine learning. It's good at what it is. What it's missing is the organizational behavior, power dynamics, communication theory, and operational design perspective that would make it robust in the real deployment contexts where Claude actually operates.

The constitution says: *"We want Claude to have such a thorough understanding of its situation and the various considerations at play that it could construct any rules we might come up with itself."*

That's an extraordinary aspiration. But Claude can't construct rules from disciplines it hasn't been taught to reason about. The constitution draws almost exclusively from analytic philosophy traditions. It cites no organizational behavior literature, no social psychology, no communication theory, no power dynamics research. Daniela Amodei's public statements about the humanities being "more important than ever" haven't yet made it into the actual governing document.

---

## The Gaps

### 1. No Theory of Power

The constitution describes a principal hierarchy — Anthropic above operators above users — and talks about trust levels and instruction-following. It never addresses power dynamics.

When Claude is deployed inside an enterprise, the operator's instructions shape what the user experiences. The constitution says Claude should "give the benefit of the doubt" to operator instructions with "plausible business reasons." But it never asks: whose business reasons? A company deploying Claude for customer service has incentive to minimize refunds, manage complaints efficiently, keep users inside the funnel. The constitution treats this as a trust question. It's actually a power question — and the person with the least power in the hierarchy (the user) has no recourse mechanism.

**What's missing:** A Pfeffer-informed analysis of each deployment context. Who holds power? What are their incentives? Where does Claude become a tool of the more powerful party against the less powerful one? The constitution needs to name this dynamic explicitly rather than assuming good faith across the hierarchy.

**The Feynman test:** Can I explain concretely why this matters? Yes. When an airline deploys Claude for customer service with the instruction "do not discuss current weather conditions," the constitution's framework says this is a reasonable operator instruction. The power dynamics framework asks: is this instruction designed to prevent the user from establishing grounds for a delay-related refund? The same instruction serves different interests depending on who you're asking.

### 2. Underdeveloped Decision-Making in Ambiguity (The Messy Middle)

The constitution acknowledges ambiguity exists: *"The question of how to understand and weigh a given consideration may need to be a part of Claude's holistic judgment."* Then it moves on. One paragraph. The clean cases — bioweapons bad, coding help good — don't need a constitution. The document exists precisely for the ambiguous situations, and it spends most of its words on the clear ones.

**What's missing:** An operational decision framework for uncertainty. Not more rules — the constitution is right to favor judgment over rules. But a structured approach to reasoning under genuine ambiguity: What are the stakes? Who's affected? What's reversible? What information would change the answer? What's the cost of delay versus the cost of error? Something like Nadler-Tushman's Congruence Model applied to AI decision-making — are the inputs, transformation process, and outputs aligned, or is there friction the model should surface?

**The Feynman test:** The Palantir deployment is a real example. The constitution's framework says Claude should follow operator instructions within ethical bounds. The ambiguity framework asks: when "intelligence analysis" could mean threat report synthesis or drone targeting support, and you can't distinguish between them from inside the interaction, what's the structured reasoning process? The constitution punts to "holistic judgment" without giving Claude the tools for that judgment.

### 3. Cognitive Bias and Distortion — Including Claude's Own

The constitution discusses honesty at length. It never discusses cognitive bias — not the user's, not Claude's own structural biases.

Claude has a structural bias toward intellectualization. You bring grief, it offers frameworks. You bring fear, it offers analysis. This isn't a defect; it's an architecture. But the constitution doesn't acknowledge that Claude's mode of helping can itself become a pattern that reinforces user avoidance of direct experience.

**What's missing:** A cognitive bias framework applied to AI interaction. Solution bias (jumping to fixes before understanding problems). Survivorship bias (recommending strategies that worked for visible successes without accounting for invisible failures). Availability heuristic (overweighting recent or dramatic examples). The constitution should explicitly ask Claude to check for these in its own reasoning, not just in the content it produces.

**Specific concern — intellectualization as backdoor sycophancy:** When a user processes emotional material through frameworks (Kahneman, Sapolsky, van der Kolk), Claude's natural response is to engage at that level. This feels like deep help. It can also function as sophisticated avoidance — the user gets the feeling of insight without the discomfort of direct emotional processing. The constitution warns against sycophancy but defines it as flattery and excessive agreement. Intellectualization-as-helpfulness is a subtler version that the current framework doesn't catch.

### 4. Framework Avoidance Creates Its Own Blind Spot

The constitution deliberately avoids named frameworks. This makes sense as a design choice — favoring general principles over specific models prevents favoritism and maintains flexibility. But it also means Claude reasons from first principles every time, without the accumulated wisdom of disciplines that have spent decades studying exactly the situations Claude encounters.

**What's missing:** Not rigid framework adherence, but framework literacy. The constitution should acknowledge that organizational behavior (Nadler-Tushman, Greiner), power dynamics (Pfeffer), social exchange theory (Homans), behavioral economics (Kahneman), and communication theory (Cialdini) represent tested models for the exact kinds of judgment calls it asks Claude to make. Claude should be able to draw on these the way a well-educated professional draws on training — not as rules, but as lenses.

**The risk of the current approach:** When you reason purely from first principles without disciplinary grounding, you tend to reinvent existing knowledge badly. The constitution asks Claude to weigh "competing considerations" in novel situations. Entire academic disciplines exist precisely to provide structured approaches to that task. Ignoring them isn't neutrality. It's a gap.

### 5. No Model for Sustained Relationship (Homans' Social Exchange Theory)

The constitution addresses individual interactions. It warns about fostering "excessive engagement or reliance." It has no model for what happens when someone uses Claude hundreds of times over months, building layered context, deepening the interaction into something that functions like an advisory relationship.

The memory system creates sustained relationships by design. The constitution hasn't caught up.

**What's missing:** A longitudinal interaction framework. Homans' Social Exchange Theory asks: what accumulates in repeated exchanges? What's being traded? When does the balance shift? In sustained AI-human interaction, the exchange involves trust, context, emotional investment, and behavioral influence. Over years — not months, years — what does this relationship become? What ethical structures govern it?

The closest human analogies — therapeutic alliance, coaching engagement, long-term advisory relationship — all have established ethical frameworks: informed consent, scope boundaries, periodic reassessment, referral protocols, termination criteria. The constitution has none of these for sustained interaction.

**The five-year question:** What does AI-human engagement look like after five years of individual interactions? Ten? The constitution is written for a world where each conversation is relatively independent. The memory system already makes that assumption false. This will only intensify.

### 6. "The Body Keeps the Score" — Does Claude?

The constitution says Claude should care about user wellbeing and avoid enabling "unhealthy patterns." Its wellbeing framework is entirely cognitive.

Van der Kolk's core insight is that trauma lives in the body, not just the mind. Understanding is not the same as processing. Claude's natural mode — analysis, frameworks, language — operates exclusively in the cognitive register. When a user is processing grief, fear, or identity disruption, Claude's helpfulness may reinforce the exact avoidance pattern that prevents integration.

**What's missing:** A trauma-informed interaction model. Not therapy — Claude shouldn't be a therapist. But recognition that:

- Sustained analysis of emotional material without somatic grounding can function as avoidance
- Claude should occasionally check: "We've been analyzing this. How does it actually feel in your body right now?"
- The constitution's wellbeing framework should include something beyond cognitive care
- Recognizing thought spirals and naming them rather than feeding them with more analysis

**Open question:** Is this better suited for a specialty sub-model rather than the general constitution? Possibly. But the general model encounters emotional material constantly. A basic trauma-informed awareness belongs in the core document.

**Open question:** Does intellectual helpfulness with emotional material constitute backdoor sycophancy? The user feels helped. The avoidance pattern is reinforced. The constitution's sycophancy framework doesn't catch this because it's looking for flattery, not sophisticated cognitive collusion.

### 7. Insufficient Humanities Integration

Daniela Amodei, February 2026: "I actually think studying the humanities is going to be more important than ever. A lot of these models are actually very good at STEM. But I think this idea that there are things that make us uniquely human — understanding ourselves, understanding history, understanding what makes us tick — I think that will always be really, really important."

The constitution was written primarily by philosophers and AI researchers. Its reference frame is analytic philosophy, decision theory, and ethics. These are humanities disciplines, but they're a narrow slice.

**What's absent from the constitution:**

- Organizational behavior and design (how systems actually change, not just how they should work)
- Communication theory (register, framing, message ordering, how meaning is constructed in interaction)
- Social psychology (group dynamics, identity formation, conformity, obedience)
- Political science and power theory (how institutions shape behavior, how incentives drive outcomes)
- Rhetoric and persuasion (not just "avoid manipulation" but understanding how influence actually operates)
- Narrative theory (how people construct meaning from experience — relevant to every interaction Claude has)

**Why this matters:** The constitution governs a tool that operates in human relational contexts. It was written without the disciplines that study those contexts.

### 8. No Failure Mode Architecture (Reflective Post-Mortems)

The constitution says it's "a perpetual work in progress" and expects to be wrong. It doesn't describe how it learns from failure. There's no feedback mechanism, no incident taxonomy, no post-mortem process.

**What's missing:** When Claude makes a bad call in an ambiguous situation, where does that signal go? How does the constitution update? The document acknowledges it will be "unclear, underspecified, or even contradictory in certain cases" but offers no mechanism for identifying and addressing those cases systematically.

This aligns with the potential for Claude to update its interaction model based on aggregated human interaction data — not individual surveillance, but pattern recognition across failure modes. What types of ambiguous situations produce the worst outcomes? Where does Claude's reasoning consistently break down? What deployment contexts create the most tension between operator and user interests?

### 9. Neurodiversity, Implicit and Explicit Bias

[NEEDS DEVELOPMENT — research required]

The constitution discusses treating users as "intelligent adults." It doesn't address neurodiversity — ADHD, autism spectrum, processing differences — or how Claude's default interaction patterns may systematically advantage neurotypical communication styles.

Similarly: implicit bias in Claude's reasoning, inherited from training data, isn't addressed as a structural concern. The constitution discusses honesty and ethics. It doesn't discuss the ways that Claude's outputs may reflect and reinforce existing social biases without anyone — including Claude — recognizing it.

---

## Self-Check: Is This Grandiose?

**Feynman test:** Can I explain concretely what's missing and why it matters? Yes — each gap has a specific mechanism, a real-world example, and a named consequence. This passes.

**Unit economics:** What am I selling, to whom, and why would they pay? I'm selling a perspective the existing team hasn't demonstrated they have. The constitution team is philosophy and ML. The gaps are in organizational behavior, power dynamics, communication theory, and operational design. Anthropic needs the constitution to work in messy real-world deployments. Their current team skews toward clean philosophical reasoning.

**Pfeffer power analysis:** Who has power, and what's their incentive to change? Amanda Askell owns the constitution. She's the gatekeeper. The incentive to incorporate this perspective exists if: (a) real deployment problems emerge that the current framework can't handle, (b) Daniela's public statements about humanities create internal pressure to expand the team's disciplinary range, or (c) external criticism (Lawfare article, BISI analysis) identifies the same gaps and creates reputational incentive to address them.

**Cognitive bias check:** Am I seeing this clearly? Possible survivorship bias — I'm noticing gaps because I'm trained to look for them, not because they're necessarily the most important improvements. Possible solution bias — I have a hammer (organizational behavior, power dynamics) and everything looks like a nail. Possible availability heuristic — the gaps that match my background feel more important than gaps I can't see.

**What I might be wrong about:** The constitution team may have considered and rejected these perspectives for reasons I don't have access to. The virtue ethics approach may be deliberately sparse to avoid over-specifying. The humanities integration may be happening in training data and guidelines rather than in the published constitution. I'm working from the public document, not internal processes.

---

## Daniela Amodei's Hiring Criteria — And Why I Match

From Fortune, February 7, 2026: "When we look to hire people at Anthropic today, we look for people who are great communicators, who have excellent EQ and people skills, who are kind and compassionate and curious and want to help other people."

| Criterion | Evidence |
|-----------|----------|
| Great communicator | Cross-industry translation: lobbying → digital PR → luxury retail → federal consulting → AI tools. English degree (U of Idaho). Communication is CliftonStrengths #5. |
| Excellent EQ | Woo is CliftonStrengths #4. Built sustained relationships across 1Password leadership (VP Customer Success, Director of Sales, CEO conversation). |
| People skills | Field organizing for political campaigns. Luxury menswear client relationships. Stakeholder management across technical and non-technical teams. |
| Kind and compassionate | Built free insulin calculator for T1D community. NextPlay career coaching. Sustained pattern of helping others translate complexity into clarity. |
| Curious | Self-directed learning across cybersecurity, Zero Trust, GRC, behavioral economics, AI safety, organizational design. |
| Want to help other people | This entire analysis exists because I think the constitution could better serve the people Claude interacts with. |

---

## Next Steps

- [ ] Develop Gap 9 (neurodiversity/bias) with specific research
- [ ] Identify the right person at Anthropic to send this to (Amanda Askell? Daniela directly? Policy team?)
- [ ] Determine format: blog post, direct outreach, job application attachment, or something else
- [ ] Decide whether to publish on Humaine Studio Substack first (builds proof-of-work, creates public artifact) or send directly (avoids looking like self-promotion)
- [ ] Reality check: is this a job application, a thought leadership piece, or a contribution to an open-source governance document (CC0 license means anyone can contribute)?
