# CLAUDE.md - Project Setup & Guidelines

*This file is automatically loaded by Claude Code to provide project context and best practices*

## Project Overview

**humaine.studio** - A Jekyll-based website hosted on GitHub Pages, showcasing the journey of learning to code with curiosity and an English/MBA background.

- **Repository**: https://github.com/miqcie/Humaine-studio
- **Live Site**: https://humaine.studio
- **Tech Stack**: Jekyll, GitHub Pages, Markdown, HTML/CSS/JS

## CRITICAL Jekyll/Markdown Rules

### ⚠️ NEVER Mix HTML Containers with Markdown Content
**Problem:** Jekyll's kramdown parser switches to HTML mode when it encounters HTML block elements, causing markdown syntax to render as literal text instead of being processed.

**❌ WRONG:**
```html
<div class="some-container">
## This heading won't render
- This list won't work
**This bold won't work**
</div>
```

**✅ CORRECT OPTIONS:**
1. **Pure Markdown** (preferred):
```markdown
## This heading renders properly
- This list works
**This bold works**
```

2. **HTML with markdown="1" attribute** (if HTML container needed):
```html
<div class="some-container" markdown="1">
## This heading will render
- This list will work
</div>
```

3. **Pure HTML** (convert everything):
```html
<div class="some-container">
<h2>This heading renders</h2>
<ul><li>This list works</li></ul>
<p><strong>This bold works</strong></p>
</div>
```

### Recent Fixes Applied
- **Cover letter page**: Removed HTML `<article>` and `<div>` wrappers, used pure markdown
- **Resume page**: Avoided HTML containers, used CSS targeting instead

## Development Environment Setup

### Required Tools
```bash
# Essential tools for this project
bundle install          # Install Jekyll dependencies
bundle exec jekyll serve # Run local development server
git status              # Check repository status
gh repo view            # View GitHub repository (requires gh CLI)
```

### Local Development
```bash
# Start local server
bundle exec jekyll serve

# Local site URL
http://localhost:4000

# Build site (GitHub Pages does this automatically)
bundle exec jekyll build
```

## Repository Structure
```
humaine.studio/
├── _config.yml          # Jekyll configuration
├── _posts/              # Published blog posts (YYYY-MM-DD-title.md format)
├── _drafts/             # Work-in-progress posts (not published)
├── _includes/           # Reusable components
├── _layouts/            # Page templates
├── assets/              # CSS, JS, images, PDFs
│   ├── css/
│   ├── js/
│   ├── images/
│   └── resume/          # Resume PDFs
├── writing-topics/      # Content planning and topic tracking
│   ├── applied-ai-topics.md   # Master topics list
│   └── notes/           # Research notes for each topic
├── scripts/             # Helper scripts (Substack mirroring, etc.)
├── docs/                # Internal documentation
├── CLAUDE.md            # This file - Claude Code context
├── .gitignore           # What not to track
└── README.md            # Public project documentation
```

## Git Workflow - ALWAYS Follow This

### CRITICAL: Never Work on Main Branch
```bash
# ALWAYS check current branch first
git branch

# ALWAYS create feature branch for changes
git checkout -b feature/descriptive-name

# ALWAYS pull latest changes first
git pull origin main
```

### Safe Commit Process
```bash
# Review changes before committing
git diff

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Action: Clear description of what changed"

# Push to feature branch
git push origin feature/descriptive-name

# Create PR on GitHub - NEVER push directly to main
```

## Testing & CI/CD

### GitHub Actions Workflows
This repository includes automated checks that run on every PR:

```yaml
# .github/workflows/jekyll-checks.yml
- Jekyll Build Verification  # Ensures site builds without errors
- HTML5 Validation          # Catches markup issues
- Accessibility Testing     # axe-core automated a11y checks  
- Performance Audit         # Lighthouse CI scores
- Link Checking            # Validates external URLs work
- Spell Check              # Content quality validation
```

### Local Testing Commands
```bash
# Test Jekyll build
bundle exec jekyll build --strict_front_matter

# Validate HTML (requires html5validator)
html5validator --root _site/

# Check accessibility (requires axe-core CLI)
npx @axe-core/cli _site --include-tags wcag2a,wcag2aa

# Test performance (requires lighthouse CLI)  
lighthouse http://localhost:4000 --chrome-flags="--headless"
```

### Configuration Files
- `.htmlhintrc` - HTML validation rules
- `lighthouserc.js` - Performance testing config
- `.spellcheck.yml` - Spell check settings
- `.github/wordlist.txt` - Approved project vocabulary

## Code Style & Standards

### Jekyll/Markdown Guidelines
- Use front matter for all posts and pages
- Date format for posts: `YYYY-MM-DD-title.md`
- Keep filenames lowercase with hyphens
- Use semantic HTML in layouts
- Optimize images before adding to assets/
- **NEVER mix HTML containers with markdown content**

### Content Guidelines
- Write in clear, accessible language
- Show learning process, including mistakes
- Include code examples when relevant
- Document decisions and reasoning

## Security Best Practices

### NEVER Commit These Items
```bash
# Items that should NEVER be in the repository
.env                    # Environment variables
config/secrets.yml      # Any secrets or API keys
private/               # Private files
*.log                  # Log files with potential sensitive data
.vscode/settings.json  # May contain local paths/tokens
```

### Safe External Integrations
```bash
# ✅ Safe for static sites
- Google Analytics (GA4)
- Formspree for contact forms
- Disqus/Utterances for comments
- CDN resources (cdnjs.cloudflare.com)

# ❌ Avoid on static sites
- Database connections from frontend
- Server-side authentication
- Direct API calls with secrets
- File uploads without proper service
```

## Common Tasks & Commands

### Creating New Content
```bash
# New blog post
touch _posts/$(date +%Y-%m-%d)-post-title.md

# New page
touch page-name.md

# Remember to add front matter to all files
```

### Testing & Validation
```bash
# Test locally before pushing
bundle exec jekyll serve

# Check for broken links (if jekyll-link-checker installed)
bundle exec jekyll build --check-links

# Validate HTML (if html-proofer installed)
bundle exec htmlproofer ./_site
```

### GitHub Integration
```bash
# Create PR from command line
gh pr create --title "Feature: Description" --body "Details about changes"

# View PR status
gh pr status

# Check GitHub Pages build status
gh workflow list
```

## Publishing Workflow: Jekyll + Substack

### Content Strategy
**Primary Platform:** Jekyll site (humaine.studio) = source of truth
**Secondary Platform:** Substack (humainestudio.substack.com) = audience growth & email distribution

**Publishing Model:** Write once in Jekyll → Mirror to Substack → Set canonical URL

### Phase 1: Planning & Topic Selection

**Location:** `writing-topics/applied-ai-topics.md`

1. Review topics list and select based on priority/interest
2. Update status: "To Do" → "In Progress"
3. Commit status change: `git commit -m "Starting [TOPIC-ID]: [Title]"`
4. (Optional) Create research notes in `writing-topics/notes/[TOPIC-ID]-notes.md`

### Phase 2: Writing Locally

**Draft Location:** `_drafts/` folder (not published until moved)

```bash
# Create new draft
cd "/Users/chrismcconnell/GitHub/Humaine Studio"
touch _drafts/post-title.md

# Add front matter
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD
categories: [category1, category2]
excerpt: "Brief description for SEO and previews"
---
```

**Writing Tips:**
- Write in markdown in your local editor (VS Code/Cursor)
- Use Claude Code for research, editing, and content generation
- Commit frequently as checkpoints: `git commit -m "Draft: Added section X"`
- Each commit = save point you can return to

**Preview Locally:**
```bash
bundle exec jekyll serve --drafts
# View at: http://localhost:4000
```

### Phase 3: Publishing to Jekyll (Automated)

**When draft is ready:**

```bash
# 1. Move from _drafts/ to _posts/ with date prefix
mv _drafts/post-title.md _posts/2025-11-25-post-title.md

# 2. Update topics list status: "In Progress" → "Published"
# Edit: writing-topics/applied-ai-topics.md

# 3. Final preview
bundle exec jekyll serve
# Verify at: http://localhost:4000

# 4. Commit and push
git add _posts/2025-11-25-post-title.md
git add writing-topics/applied-ai-topics.md
git commit -m "Publish: [Title] ([TOPIC-ID])

- [Brief description of content]
- Published to humaine.studio blog"

git push origin main
```

**Automatic Deployment:**
- GitHub Actions triggers on push
- Runs CI checks (HTML validation, a11y, performance)
- Deploys to humaine.studio (2-3 minutes)
- Post live at: `humaine.studio/posts/YYYY/MM/DD/post-title/`

### Phase 4: Mirror to Substack

**Timing:** Can be done immediately or batched weekly

```bash
# Helper script (see scripts/mirror-to-substack.sh)
./scripts/mirror-to-substack.sh "https://humaine.studio/posts/2025/11/25/post-title/"
```

**Manual Process:**
1. Open published post on humaine.studio
2. Copy markdown or HTML content
3. Log into Substack → New Post
4. Paste content into editor
5. Add Substack-specific elements:
   - Email-friendly opening hook
   - "Originally published at [URL]" footer
   - Call-to-action for subscribers
6. **CRITICAL:** Set canonical URL in post settings:
   - ☑️ "This post was originally published elsewhere"
   - Canonical URL: `https://humaine.studio/posts/.../post-title/`
7. Publish or schedule
8. Email sent to subscribers automatically

**Why Canonical URL Matters:**
- Google knows humaine.studio is the original source
- SEO credit goes to your site
- Substack serves as distribution channel

### Phase 5: Promotion (Optional)

**Can be batched weekly:**
- LinkedIn: Share with summary
- Twitter/X: Thread or link
- Direct outreach to people who'd find it valuable
- Engage with Substack comments

### ADHD-Friendly Batching Strategy

**Focus Sessions (Writing):**
- Week 1-2: Write 3-4 drafts in `_drafts/`
- Commit after each writing session

**Publishing Cadence:**
- Every Monday: Publish one post to Jekyll (automated)
- Every Friday: Batch mirror to Substack
- Weekend: Batch social promotion

**Benefits:**
- Separates creative work (writing) from distribution (publishing)
- Builds content buffer to reduce pressure
- Clear triggers reduce decision fatigue

### Time Estimates Per Post

| Activity | Time | Batchable? |
|----------|------|------------|
| Topic selection | 5 min | Yes |
| Writing first draft | 2-4 hours | No |
| Review & polish | 30-60 min | No |
| Publish to Jekyll | 2 min | No |
| Mirror to Substack | 10-15 min | **Yes** |
| Promotion | 15-30 min | **Yes** |

### Quick Reference Commands

```bash
# Start new draft
touch _drafts/$(date +%Y-%m-%d)-topic-title.md

# Preview drafts locally
bundle exec jekyll serve --drafts

# Publish draft (move to _posts with date)
mv _drafts/title.md _posts/$(date +%Y-%m-%d)-title.md

# Standard commit for published post
git add _posts/*.md writing-topics/applied-ai-topics.md
git commit -m "Publish: [Title] ([TOPIC-ID])"
git push origin main

# Helper for Substack mirroring
./scripts/mirror-to-substack.sh "[POST_URL]"
```

## Claude Code Best Practices for This Project

### Effective Prompts for This Codebase
```bash
# Good prompts - specific and contextual
claude-code "Add a new blog post about learning Claude Code, following our Jekyll post format and style guidelines"

claude-code "Update the navigation to include a new 'Tools' section, maintaining our current design patterns"

claude-code "Fix any accessibility issues in the site layout, ensuring proper semantic HTML"

# Avoid vague prompts
claude-code "make the site better"  # Too vague
claude-code "add features"          # Not specific enough
```

### Use Thinking Modes for Complex Tasks
```bash
# For complex changes, use thinking modes
claude-code "think hard about how to restructure the site architecture for better user experience"

claude-code "ultrathink: plan a comprehensive content strategy for showcasing coding journey"
```

### Multi-Step Workflow Pattern
1. **Explore**: "Read the existing [relevant files] and understand the current structure"
2. **Plan**: "Create a detailed plan for [specific change] without writing code yet"
3. **Implement**: "Now implement the plan, following our style guidelines"
4. **Test**: "Test the changes locally and fix any issues"
5. **Commit**: "Create a descriptive commit and push to feature branch"
6. **Wrap-up**: "Run `specstory sync` to document the session"

### Session End Workflow
**ALWAYS run at the end of every session:**
```bash
# Sync session history to Specstory (local only, no cloud sync)
specstory sync --no-cloud-sync
```
This documents your work and maintains a searchable history of all Claude Code sessions in `.specstory/` directory.

## Emergency Procedures

### If Something Breaks
```bash
# Revert last commit (if not pushed)
git reset --soft HEAD~1

# Revert specific file
git checkout -- filename.md

# Revert after pushing
git revert HEAD
```

### If GitHub Pages Build Fails
1. Check Actions tab in GitHub repository
2. Review error messages in failed build logs
3. Common fixes:
   - Verify `_config.yml` syntax
   - Check all posts have proper front matter
   - Ensure file paths are correct
   - Remove any problematic characters in filenames

### If CI Checks Fail
```bash
# HTML validation errors
- Check for unclosed tags, invalid attributes
- Validate front matter syntax

# Accessibility errors  
- Add alt text to images
- Ensure proper heading hierarchy
- Check color contrast ratios

# Performance issues
- Optimize image sizes
- Minimize CSS/JS files
- Remove unused dependencies

# Broken links
- Update or remove dead external links
- Fix internal relative paths
- Check markdown link syntax
```

## Project Goals & Context

### Learning Journey Documentation
- Show that curiosity beats formal CS education
- Document real learning process, including failures
- Create practical guides for other career changers
- Build in public to inspire others

### Technical Skills Development
- Jekyll static site generation
- Git workflow and best practices
- Basic HTML/CSS/JavaScript
- Command line comfort
- Claude Code integration
- CI/CD and automated testing

### IMPORTANT Reminders for Claude

1. **ALWAYS work on feature branches** - never commit directly to main
2. **Test locally first** - run `bundle exec jekyll serve` before pushing
3. **Follow the explore→plan→implement→test→commit→wrap-up workflow** for complex changes
4. **Keep security in mind** - this is a public repository
5. **Document decisions** - explain why you made specific choices
6. **Maintain accessibility** - ensure all users can access content
7. **Optimize for learning** - prioritize clear, educational content over complexity
8. **Run CI checks locally** - use testing commands before pushing
9. **Follow PR workflow** - all changes go through pull request review
10. **NEVER mix HTML containers with markdown** - use pure markdown or pure HTML
11. **ALWAYS run `specstory sync --no-cloud-sync` at session end** - documents work history automatically

## Quick Reference

### Essential Commands
```bash
git status                         # Check current status
git checkout -b feature/name       # Create new branch
bundle exec jekyll serve           # Start local server
git diff                           # Review changes
gh pr create                       # Create pull request
bundle exec jekyll build           # Test build process
specstory sync --no-cloud-sync     # Document session history (run at session end)
```

### File Locations
- Published posts: `_posts/YYYY-MM-DD-title.md`
- Draft posts: `_drafts/title.md`
- Topics list: `writing-topics/applied-ai-topics.md`
- Research notes: `writing-topics/notes/[TOPIC-ID]-notes.md`
- Helper scripts: `scripts/`
- Pages: `page-name.md` (root level)
- Layouts: `_layouts/`
- Includes: `_includes/`
- Assets: `assets/css/`, `assets/js/`, `assets/images/`, `assets/resume/`
- Config: `_config.yml`
- CI/CD: `.github/workflows/`
- Testing configs: `.htmlhintrc`, `lighthouserc.js`, `.spellcheck.yml`

---

*This file is version-controlled and shared with the team. Update it as the project evolves.*