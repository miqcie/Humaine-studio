---
layout: post
title: "Experiments in Building a GRC Tool in a Weekend"
date: 2026-01-11
categories: [security, compliance]
tags: [zero-trust, compliance, GRC, build-vs-buy, decision-framework]
excerpt: "I built a Zero Trust CI/CD prototype in 4 hours that generates cryptographic compliance proof. Here’s what I learned about fast validation and what that decision framework means for solopreneurs in GRC and cybersecurity."
---

Most people who identify a real market problem try to build a company around it. I did the opposite.

I built a working Zero Trust tool in 4 hours. It blocks risky infrastructure changes, generates cryptographically signed attestations, and integrates with GitHub Actions. The code works. The technical approach is sound. The market problem is real.

[And I’m not launching it](https://humaine.studio/posts/2026/01/11/experiments-building-grc-tool-weekend/).

This isn’t a failure story. It’s a decision framework story — one that every CISO should understand when evaluating build vs. buy decisions in security tooling. The interesting part isn’t the code. It’s the reasoning behind choosing *not* to ship it.

## The Problem: The Security Poverty Line

In 2011, Wendy Nather at 451 Research coined the term "security poverty line" - the economic threshold below which organizations cannot achieve mature security posture, regardless of effort. Fourteen years later, the data shows it's gotten worse:

**29% of organizations lose new business** due to missing compliance certifications (A-LIGN 2023). Not because their product is bad. Not because their security is weak. Because they can't afford the $200,000-$400,000 first-year cost to prove it:

- SOC 2 certification: $35K-150K initially, $12K-60K annually
- Internal engineering effort: 100-200 hours = ~$50K opportunity cost
- Insurance impact: Companies with strong security controls receive more favorable terms and pricing ([Marsh Cyber Insurance Market Update](https://www.marsh.com/en/services/cyber-risk/insights/cyber-insurance-market-update.html))
- Lost deal velocity: 41% report sales cycle slowdowns (Drata 2023 Compliance Trends Report)

I experienced this firsthand at DeepWaterPoint & Associates. We spent hundreds of hours collecting screenshots and documentation for auditors - compliance theatre that didn't meaningfully reduce risk, just checked boxes.

The question wasn't whether the problem exists. It was whether I could solve it.

## The Validation: Building Mondrian

I was accepted to Startup Virginia's Idea Factory, a pre-incubator program focused on customer discovery and early validation. The framework was clear: talk to 50+ potential customers before building anything.

I did the opposite. I spent 4 hours building first.

**What Mondrian does:**
- Scans infrastructure code (Terraform) for security violations
- Blocks risky GitHub PRs before they merge (public S3 buckets, open security groups, long-lived AWS credentials)
- Generates DSSE-signed attestations proving controls ran
- Creates tamper-evident audit trails with hash chains

The technical approach works. Evidence-first security is feasible - you can cryptographically prove that security controls ran, not just claim they did in a screenshot.

## The Data: What The Prototype Proved

**Technical validation was complete:**
- SLSA-compatible attestation format
- Dead Simple Signing Envelope (DSSE) cryptographic signatures
- GitHub Actions integration blocking risky changes
- Hash-chain integrity for tamper-evident audit logs

**Market resonance was real:**
- 96% of GRC teams struggle with compliance (Swimlane study)
- Average data breach costs $4.45M, with SMBs facing proportionally devastating costs relative to revenue ([IBM Cost of a Data Breach 2023](https://www.ibm.com/reports/data-breach))
- For a startup with $2M ARR, a $200K compliance cost represents 10% of revenue — enough to flip operating margins negative

**But competitive reality was sobering:**
- Checkov, Terrascan, and tfsec already provide free policy scanning
- Vanta and Drata already lowered compliance costs from $400K to $200K
- They solve 80% of evidence collection through SaaS integrations
- The remaining 20% (cryptographic proof) requires answering: "Do auditors actually accept this?"

## The Decision: Why Archive Instead of Launch

I had the technical pieces. I had quantified market data. I had a clear positioning: "PostHog for Zero Trust - make enterprise security accessible without enterprise budgets."

What I didn't have: 50 customer discovery interviews validating demand.

**The Startup Virginia framework was right, and I ignored it.** Build first, validate later - classic founder mistake. But the framework's rigor revealed something more valuable: a mismatch between the work required and my actual strengths.

**What OSS product maintenance requires:**
- Ongoing community building and developer evangelism
- Sustained customer development (50+ interviews, continuous feedback loops)
- Product management and roadmap prioritization
- Support and documentation maintenance
- Sales outreach for enterprise adoption

**What I'm actually good at:**
- Fast prototyping to validate technical feasibility
- Translation and synthesis (compliance → engineering language)
- Strategic analysis (build/buy/partner decision frameworks)
- Content creation that reaches broader audiences

The moment of clarity: I had customer discovery paralysis. Not because I couldn't talk to people - I can. But because deep down, I knew community-building wasn't where I'd create the most value.

**Then family health shifted priorities.** My kid was diagnosed with Type 1 Diabetes a few weeks after building Mondrian. Suddenly the 12-18 month SBIR research commitment I'd planned for became impossible.

But the deeper reason was already there: **advisory/content work creates more impact for my skill set than OSS product maintenance.**

## The Lesson: Fast Prototyping for Validation, Not Commitment

Here's what I got right:

**✅ Fast validation beats slow planning** - 4 hours proved technical feasibility without months of architecture docs

**✅ Documentation captures value** - PROJECT_REPORT.md, RETROSPECTIVE.md, and technical specs preserve learnings

**✅ Evidence-first approach is sound** - The technical pieces exist (SLSA, DSSE, Sigstore), integration is the gap

**✅ Market framing resonates** - "Security poverty line" cuts through noise better than feature lists

Here's what I missed:

**❌ Customer validation comes first** - Should have talked to 20 security leaders before writing any code

**❌ Competitive moat analysis matters** - "Why hasn't Vanta/Drata added crypto attestations?" is the critical question

**❌ Match work to strengths** - Community-building misalignment should have been obvious earlier

**❌ Honest ROI analysis upfront** - Advisory model gives flexibility; OSS maintenance locks in commitment

## What This Means for CISOs

Every CISO faces build vs. buy decisions. The conventional wisdom is "buy when possible, build when differentiation matters." But that misses the nuance:

**Build to validate, not to launch.** Rapid prototyping can answer critical questions:
- Is this technical approach feasible?
- Does our team have the skills to maintain this?
- What's the actual effort required vs. vendor solution?

**Partner when vendors solve 80%.** Vanta and Drata lowered compliance costs by 75%. The remaining gap (cryptographic attestations) might not justify building a competitive solution.

**Advise when translation matters more than code.** Sometimes the highest-value work is helping others make better decisions, not building the thing yourself.

## The Best Product Decision is Sometimes No Product At All

Mondrian validates an approach. It doesn't become a company. The code lives as an open-source reference (github.com/miqcie/mondrian, archived January 2026). The insights become blog posts and advisory frameworks.

**This isn't a failure - it's strategic repositioning.** I can help more organizations by:
- Validating technical approaches quickly (proof-of-concept in hours, not months)
- Translating compliance requirements into engineering reality
- Making honest build/buy/partner recommendations
- Sharing frameworks publicly instead of maintaining private codebases

For CISOs: **prototype to validate ideas, not to commit.** Build small, learn fast, and be ruthlessly honest about where your team's strengths create the most value.

Sometimes that means building a product. Sometimes it means advising others on what to build. And sometimes - like Mondrian - it means validating an approach and moving on.

---

**Related Reading:**
- [The Security Poverty Line: Why Startups Can't Compete on Compliance](/posts/2026/03/02/security-poverty-line/) - Economic analysis with quantified data
- [Evidence-First vs Detection-Only Security](/posts/2026/03/02/evidence-first-vs-detection-only-security/) - Technical deep-dive into Mondrian's implementation

**For advisory/consulting inquiries** about compliance automation, evidence-first security, or build/buy decisions in the security space: [Eagle Ridge Advisory](https://eagleridge.io) | [Humaine Studio](https://humaine.studio)

**GitHub:** [miqcie/mondrian](https://github.com/miqcie/mondrian) (archived read-only reference)
