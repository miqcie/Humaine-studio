# Post-Mortem: When Automation Costs More Than Manual Work

**Date:** 2025-12-12
**Task:** Delete 24 inactive "Hide My Email" addresses on Apple's account page
**Time spent:** ~1.5 hours
**Manual time estimate:** ~5 minutes (24 emails × 3 clicks × 5 seconds)
**Outcome:** Abandoned automation, did it manually

## What Happened

I wanted to clean up 24 inactive Hide My Email addresses on Apple's account management page. The web UI has a bug where it hangs on "Updating..." after each deletion (even though the backend succeeds). I thought: "Perfect use case for Playwright automation - handle the buggy UI, batch the deletions."

I had Claude Code help me build it. We used the Jam.dev MCP to capture DOM selectors from a screen recording. The script successfully:
- Logged in via 1Password CLI integration
- Handled Apple's iframe-based auth
- Waited for 2FA approval
- Opened the inactive emails modal
- Found 200+ email rows

Then it fell apart. Multiple rounds of:
1. Wrong selectors (active emails vs inactive)
2. CSS syntax errors in Playwright locators
3. Mismatched URLs (account.apple.com vs icloud.com)
4. Rewrites that broke working code

## The Core Mistakes

### 1. No Upfront ROI Calculation
Before writing any code, I should have asked: "Is this worth automating?"

```
Manual: 24 items × 3 clicks × 5 sec = 6 minutes
Automation: Unknown, but "simple Playwright script" = 30 min estimate
Break-even: Never (one-time task)
```

The only valid reasons to automate this:
- It's a recurring task (it's not)
- The count is 100+ items (it was 24)
- Learning Playwright patterns (fair, but expensive lesson)

### 2. Chasing the Wrong Abstraction
When the Jam recording showed `icloud.com` instead of `account.apple.com`, I rewrote the entire login flow instead of asking: "Wait, which URL actually works?"

The working code got replaced with broken code because I optimized for the wrong information.

### 3. No Incremental Testing
Each code change should have been tested before the next. Instead:
- Changed selectors → didn't test
- Changed URL → didn't test
- Changed delete logic → didn't test
- Ran script → multiple failures stacked

### 4. Debugging Tools Added Too Late
Playwright has excellent debugging:
- `context.tracing.start()` captures DOM snapshots
- `page.screenshot()` at each step
- `npx playwright show-trace trace.zip` for replay

I added tracing after 1+ hour of blind debugging. Should have been there from the start.

### 5. Token/Context Burn
Each failed run triggered:
- Screenshot reads
- Jam MCP calls for new recordings
- Multiple file edits
- Long explanations

A tighter feedback loop (user runs script in terminal, reports error, I fix) would have saved significant context.

## What I Should Have Done

### Option A: Just Do It Manually (Best)
Open the page, click through 24 emails. Done in 5 minutes. Move on with life.

### Option B: Smarter Automation Approach
If automation was truly warranted:

1. **Start with tracing enabled** - debug tools from line 1
2. **Test each step in isolation** - login script, then find-rows script, then delete script
3. **Use Playwright Codegen** - `npx playwright codegen account.apple.com` records your clicks as code
4. **Set a time box** - "If this isn't working in 20 minutes, I'll do it manually"

### Option C: Different Tool Entirely
For repetitive clicking tasks, simpler tools exist:
- **Keyboard Maestro** (macOS) - record and replay clicks
- **Browser macros** - iMacros, Selenium IDE
- **AppleScript** + System Events - native macOS automation

These don't require understanding DOM structure or Playwright's selector syntax.

## Lessons for AI-Assisted Coding

### When to Use AI for Automation
- ✅ Complex, repeating workflows
- ✅ Tasks requiring data transformation
- ✅ Integration between multiple systems
- ❌ One-time manual tasks under 15 minutes
- ❌ Unstable/dynamic UIs without API access
- ❌ When you'd need multiple auth flows

### Red Flags to Abandon Ship
- Third selector rewrite
- "Let me try a different approach" more than twice
- Debugging taking longer than estimated task time
- Context window filling with failed attempts

### Better AI Collaboration Patterns
1. **Ask for effort estimate first** - "How long will this take vs. manual?"
2. **Request debugging tools upfront** - "Add tracing and screenshots from the start"
3. **Run tests yourself** - Don't burn tokens on "checking output"
4. **Set explicit time boxes** - "We have 20 minutes, then we bail"

## The Meta-Lesson

Automation has a seductive appeal: "I'll save time forever!" But most tasks aren't forever. They're once.

The sunk cost fallacy kicked in hard here. After 30 minutes, abandoning felt like "wasting" the work. But continuing wasted more.

**The best automation is often no automation.**

---

*Written after manually deleting 24 emails in 4 minutes.*
