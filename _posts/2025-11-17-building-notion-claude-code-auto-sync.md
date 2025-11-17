---
layout: post
title: "Building Auto-Sync Between Notion and Claude Code: Part 2"
date: 2025-11-17 16:00:00 -0600
categories: [ai tools, notion, automation, claude code]
tags: [claude, notion, api, integration, automation, mcp, developer tools]
excerpt: "Part 2: Taking the Notion-Claude connection further with automatic task synchronization, production-ready error handling, and security hardening. A technical deep-dive into building reliable automation."
---

## Building on the Foundation

In a [previous post about connecting Claude to Notion with MCP](/posts/2024/08/10/connecting-claude-to-notion-with-mcp), I showed how to use MCP to set up a basic connection between Claude Desktop app and Notion. The goal was to show how easy it was.

And a few months later, the capabilities of the Notion MCP is way WAY greater. Also in this time I've shifted most of my work to Claude Code CLI. So I needed to evolve how I interfaced with Notion.

A quick tangent: 

When I was in middle school in the mid-90's, I remember learning BASIC. There was a math game about optimization running a snack stand at a football stadium. You can to input variables for hotdogs, soda pops, hot chocolate, and popcorn. You didn't know the weather and how it would affect the result. I really enjoyed that game, but I didn't have the patience to learn programming. A few years (decades) later and the technology has "caught up" to my brain!

This post is **Part 2**: advancing MCP connections to help sync work across multiple tools. The goal is **automatic task synchronization**. If you're comfortable with the command line and want to see what production-ready automation looks like (including the unglamorous parts like error handling and security), this is for you.

### What's Different from Part 1?

**Part 1** (August 2024): Setting up the MCP connection
- Manual queries to Notion from Claude Desktop
- Understanding the basics
- Getting comfortable with API concepts

**Part 2** (This post): Building automation
- Automatic sync on every session start
- Production-ready error handling
- Security hardening and validation
- Project organization and maintenance
- Real technical review and fixes

Think of Part 1 as "learning to drive" and Part 2 as "building a self-driving car"—you need the fundamentals first, then you can tackle automation.

## The Problem

I use Notion for task planning across multiple projects, but when working in Claude Code, I need those tasks available in the `/todos` system. Manually copying tasks between systems is tedious and error-prone. I wanted automatic synchronization that:

1. Fetches active tasks from Notion on every session start
2. Handles errors gracefully without blocking my workflow
3. Keeps my credentials secure
4. Stays maintainable as the system evolves

## The Solution: Phase 1 - One-Way Auto-Sync

I built a system with three components:

### 1. Sync Script (`sync-notion-todos.js`)

A Node.js script that:
- Connects to Notion's API using the official `@notionhq/client`
- Queries my tasks database for active items (Not started, In progress)
- Maps Notion's rich status system to Claude Code's simpler format
- Outputs JSON compatible with TodoWrite tool

**Key features:**
- 10-second timeout to prevent hanging
- Token validation before API calls
- Proper error messages instead of cryptic failures
- Priority-based sorting (High → Medium → Low)

### 2. SessionStart Hook (`auto-sync-notion.sh`)

A bash script that runs automatically when Claude Code starts:
- Pulls Notion token securely from 1Password
- Runs the sync script in the background
- Captures errors to a secure temp file
- Reports status without blocking session start
- Sets proper file permissions (owner-only access)

### 3. Slash Command (`/sync-notion`)

A Claude Code command to load synced tasks:
- Reads the JSON file created by auto-sync
- Uses TodoWrite to load tasks into the current session
- Shows summary of task count and status breakdown

## The Technical Review

Before enabling auto-sync, I ran the implementation through a comprehensive technical review using the `gilfoyle-tech-reviewer` agent. The review found **5 critical issues** and **8 high-priority problems** that would have caused production failures.

### Critical Issues Fixed

**1. Silent Failures**
```bash
# ❌ BEFORE: All errors hidden
node sync-script.js > /dev/null 2>&1

# ✅ AFTER: Errors captured and reported
if ! node sync-script.js 2>"$ERROR_LOG"; then
  ERROR_MSG=$(cat "$ERROR_LOG" | head -1)
  echo "❌ Sync failed: ${ERROR_MSG}"
fi
```

**2. No Timeout Protection**
```javascript
// Added 10-second timeout to prevent hangs
const TIMEOUT_MS = 10000;
const timeoutHandle = setTimeout(() => {
  console.error('❌ Sync timed out after 10 seconds');
  process.exit(1);
}, TIMEOUT_MS);
```

**3. Token Validation**
```javascript
// Validate token format before API calls
if (!/^ntn_[A-Za-z0-9]{46}$/.test(process.env.NOTION_TOKEN)) {
  console.error('❌ Invalid NOTION_TOKEN format');
  process.exit(1);
}
```

**4. File Permission Vulnerabilities**
```bash
# Protect temp files from other users
chmod 600 /tmp/claude-todos.json
chmod 600 "$ERROR_LOG"
```

**5. Error Reporting**
```javascript
// Clear feedback on what went wrong
syncToClaudeCode().catch(err => {
  console.error('❌ Sync failed:', err.message);
  process.exit(1);
});
```

## Project Organization

Initially, I had scripts scattered in my home directory. Following best practices, I reorganized everything under `~/.claude/notion-sync/`:

```
~/.claude/
├── notion-sync/              # All sync files organized here
│   ├── .gitignore           # Prevent committing sensitive files
│   ├── INDEX.md             # Quick reference guide
│   ├── README.md            # Full documentation
│   ├── SETUP.md             # Implementation details
│   ├── sync-notion-todos.js # Main sync script
│   └── notion-todo-sync.js  # Analysis tool
├── hooks/
│   └── auto-sync-notion.sh  # SessionStart hook
├── commands/
│   └── sync-notion.md       # Slash command definition
└── settings.json            # Hook configuration
```

**Why this matters:**
- All related files live together
- Easy to backup or migrate
- Clear documentation hierarchy
- Discoverable for future me

## What I Learned

### 1. Error Handling is 80% of the Code

The "happy path" (everything works perfectly) was easy to build. The hard part was handling:
- Network timeouts
- Invalid credentials
- Empty databases
- Permission errors
- Concurrent access

**Lesson**: Always ask "what happens when this fails?" before shipping.

### 2. Silent Failures Are Worse Than Loud Ones

My initial implementation used `> /dev/null 2>&1` to suppress output. This meant when things broke, I had zero feedback. The fixed version:
- Captures errors explicitly
- Shows clear error messages
- Logs to secure temp files
- Never blocks the session start

**Lesson**: Debugging is impossible without observability.

### 3. Security Requires Intentional Design

Several security issues emerged:
- Tokens visible in process list
- World-readable temp files
- No credential validation

**Fixes applied:**
- Secure temp files with `mktemp` and `chmod 600`
- Token format validation before use
- Process cleanup with `trap` handlers

**Lesson**: Security isn't a feature you add later—it's baked into architecture.

### 4. Documentation is Future You's Best Friend

I created three levels of documentation:
- `INDEX.md` - Quick reference (30 seconds)
- `README.md` - Usage guide (5 minutes)
- `SETUP.md` - Implementation details (deep dive)

**Why three files?**
- Different use cases need different depths
- Quick answers vs. full context
- Maintainability over time

### 5. One-Way Sync is Intentionally Limited

The system only syncs Notion → Claude Code, not bidirectional. This was a deliberate choice:
- Simpler to implement correctly
- Fewer failure modes
- Easier to reason about data flow
- No conflict resolution needed

**Trade-off**: I manually update Notion when completing tasks in Claude Code. That's acceptable for Phase 1.

## Current Limitations & Future Work

### Limitations
1. **One-way sync only** - No write-back to Notion yet
2. **Manual load step** - Must run `/sync-notion` after session starts
3. **No caching** - Hits API every time even if nothing changed
4. **All active tasks** - No filtering by project or category yet

### Phase 2 Roadmap
If I need bidirectional sync:
- Track Notion page IDs in todo metadata
- Implement write-back on task completion
- Add conflict resolution logic
- Handle concurrent modifications

**Estimated complexity**: 2-3 days vs. 4 hours for Phase 1.

## Technical Stack

- **Language**: Node.js (for Notion API), Bash (for hooks)
- **API**: Notion's official JavaScript SDK
- **Auth**: 1Password CLI for secure credential storage
- **Integration**: Claude Code MCP system
- **Documentation**: Markdown

## How to Use It

```bash
# Auto-sync runs on session start automatically
claude

# You'll see:
# 📋 56 active tasks synced from Notion. Run /sync-notion to load them.

# Load tasks when ready
/sync-notion

# Or test manually
NOTION_TOKEN=$(op read "op://Private/Notion MCP API Credentials/credential") \
  node ~/.claude/notion-sync/sync-notion-todos.js
```

## Resources

- **Code**: `~/.claude/notion-sync/` (see INDEX.md for structure)
- **Notion API**: [developers.notion.com](https://developers.notion.com)
- **Claude Code MCP**: [code.claude.com/docs](https://code.claude.com/docs)
- **1Password CLI**: [developer.1password.com/docs/cli](https://developer.1password.com/docs/cli)

## Reflections

This project reinforced that **building something that works** is different from **building something that works reliably in production**. The gap between those two states is:

1. Comprehensive error handling
2. Security considerations
3. Proper testing
4. Clear documentation
5. Thoughtful organization

The technical review was brutal but invaluable. It caught issues that would have caused mysterious failures weeks later when I'd forgotten how the system worked.

**Most important lesson**: Engineering isn't just making code run—it's making code run **correctly, securely, and maintainably** over time.

---

## Series Navigation

- **[Part 1: Connecting Claude to Notion with MCP](/posts/2024/08/10/connecting-claude-to-notion-with-mcp)** - Setting up the basic connection (beginner-friendly)
- **Part 2: Building Auto-Sync** - This post - Production-ready automation (intermediate/advanced)
- **Part 3: Bidirectional Sync** - Coming soon - Writing tasks back to Notion with conflict resolution

*This post is part of my journey learning to code with curiosity. If you're building similar integrations or have questions about the implementation, feel free to [reach out](https://humaine.studio/#contact).*

**Tools used**: Claude Code, Notion API, 1Password CLI, Node.js, Bash
**Time invested**: ~4 hours (Phase 1), saved countless hours of manual task copying
**Status**: ✅ Production ready (with caveats documented above)
**Prerequisites**: Read [Part 1](/posts/2024/08/10/connecting-claude-to-notion-with-mcp) first if you're new to Notion MCP
