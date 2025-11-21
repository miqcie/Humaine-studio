# CLAUDE.md - Project Setup & Guidelines

*This file is automatically loaded by Claude Code to provide project context and best practices*

## Project Overview

**humaine.studio** - A Jekyll-based website hosted on GitHub Pages, showcasing the journey of learning to code with curiosity and an English/MBA background. Serves as a research portfolio, career showcase, and educational tools platform.

- **Repository**: https://github.com/miqcie/Humaine-studio
- **Live Site**: https://humaine.studio
- **Tech Stack**: Jekyll, GitHub Pages, Markdown, HTML/CSS/JS, React/Vite (experiments)
- **Analytics**: PostHog (privacy-focused), Apollo.io (visitor intelligence)
- **CI/CD**: GitHub Actions (build, test, deploy, validation)

### Site Functions
- **Research Portfolio**: Blog posts on AI, automation, and technical topics
- **Career Showcase**: PostHog cover letter, resume, professional experience
- **Educational Tools**: T1D insulin calculator with localStorage persistence
- **Experiments**: React/Vite applications under `/experiments/` directory

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
- **Asset serving**: Added `.nojekyll` at repository root for proper GitHub Pages static asset serving

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
├── Root Configuration Files
│   ├── _config.yml               # Jekyll configuration (site metadata, plugins, analytics)
│   ├── Gemfile                   # Ruby gem dependencies (github-pages, jekyll plugins)
│   ├── CNAME                     # Custom domain (humaine.studio)
│   ├── robots.txt                # SEO crawler directives
│   ├── .gitignore                # Git exclusions
│   ├── .nojekyll                 # GitHub Pages asset serving marker
│   ├── .htmlhintrc               # HTML validation rules
│   ├── .spellcheck.yml           # Spell check configuration
│   └── lighthouserc.js           # Performance testing config
│
├── Root Pages (Served at domain root)
│   ├── index.md                  # Homepage (hero, philosophy, research, writing)
│   ├── calculator.md             # T1D insulin calculator interface
│   ├── posthog-cover-letter.md   # PostHog TAE/Manager cover letter
│   ├── privacy.md                # Privacy policy (PostHog/Apollo.io disclosure)
│   └── weeks-of-life.html        # Life weeks visualization tool
│
├── Jekyll Core Directories
│   ├── _posts/                   # Blog posts (YYYY-MM-DD-title.md format)
│   │   ├── 2021-02-20-ai-inequality-digital-future-of-work.md
│   │   ├── 2024-08-10-connecting-claude-to-notion-with-mcp.md
│   │   ├── 2024-08-11-building-humaine-studio-with-jekyll.md
│   │   ├── 2025-08-18-gilfoyle.md
│   │   ├── 2025-08-19-linkedin-certifications-posthog.md
│   │   └── 2025-11-17-building-notion-claude-code-auto-sync.md
│   │
│   ├── _layouts/                 # Page templates
│   │   ├── default.html          # Base layout (header, main, footer, analytics)
│   │   ├── home.html             # Homepage wrapper
│   │   └── post.html             # Blog post template
│   │
│   ├── _includes/                # Reusable components
│   │   ├── head.html             # <head> section (SEO, fonts, structured data)
│   │   ├── header.html           # Navigation (logo, menu, dark mode toggle)
│   │   └── footer.html           # Footer (links, copyright)
│   │
│   └── assets/                   # Static files
│       ├── css/
│       │   ├── main.css          # Global styles (theme, typography, dark mode)
│       │   └── calculator.css    # Calculator-specific styles
│       ├── js/
│       │   ├── main.js           # Theme management, smooth scrolling, PostHog
│       │   └── calculator.js     # Insulin calculation engine (localStorage)
│       ├── images/
│       │   ├── favicon-32x32.png
│       │   ├── apple-touch-icon.png
│       │   └── posts/            # Blog post images
│       └── resume/
│           └── Chris_McConnell_PostHog_TAE.pdf
│
├── Experiments (React/Vite Applications)
│   └── experiments/
│       └── invoice-collab/       # Invoice collaboration experiment
│           ├── index.html        # Built Vite app entry point
│           ├── .nojekyll         # Prevent Jekyll processing
│           ├── vite.svg          # Vite logo
│           └── assets/
│               ├── index-*.css   # Compiled CSS (hash-versioned)
│               └── index-*.js    # Compiled JavaScript (hash-versioned)
│
├── GitHub Actions & CI/CD
│   └── .github/
│       ├── workflows/
│       │   ├── jekyll-checks.yml # Main CI (build, HTML, a11y, perf, links, spell)
│       │   ├── jekyll.yml        # GitHub Pages deployment
│       │   └── link-check.yml    # Weekly link validation (Lychee)
│       └── wordlist.txt          # Spell-check approved terms
│
├── Documentation & Context
│   ├── docs/
│   │   └── calculator-roadmap.md # T1D calculator feature roadmap
│   ├── CLAUDE.md                 # This file - Claude Code context
│   ├── README.md                 # Public project documentation
│   ├── llm.txt                   # LLM optimization metadata
│   └── SESSION_CONTEXT.md        # Ongoing development session notes
│
└── Session History (.gitignored)
    └── .specstory/               # Claude Code session history
        ├── .project.json         # Project metadata
        └── history/              # Session logs (JSON format)
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
This repository includes automated checks across three workflow files:

#### **jekyll-checks.yml** (Main CI Pipeline)
**Triggers**: Push to main/feature/*, PRs to main

**Build Phase**:
- Ruby 3.1 with bundler caching
- Node 18 for testing tools
- `bundle exec jekyll build --strict_front_matter`
- Sets `JEKYLL_ENV=production` and `LANG=C.UTF-8` (UTF-8 encoding fix)

**Quality Checks** (all run in parallel):
1. **HTML Validation**: htmlhint + HTML5 validator (blocks merge)
2. **Accessibility**: axe-core CLI with WCAG 2a/2aa tags (blocks merge)
3. **Link Checking**: Markdown link checker (blocks merge)
4. **Spell Check**: pyspelling (`continue-on-error: true` - non-blocking)
5. **Performance**: Lighthouse CI (`continue-on-error: true` - non-blocking)

**Notes**:
- Spell check is non-blocking until wordlist refined (Issue #19)
- Lighthouse CI is non-blocking until 404 errors fixed (Issue #20)
- UTF-8 encoding fix prevents Jekyll build failures (from #22)

#### **jekyll.yml** (Deployment Pipeline)
**Triggers**: Push to main, manual workflow_dispatch

**Steps**:
1. Build with Jekyll (`bundle exec jekyll build`)
2. Upload artifact to GitHub Pages
3. Deploy using `actions/deploy-pages@v4`

**Permissions**: contents:read, pages:write, id-token:write

#### **link-check.yml** (Weekly Link Validation)
**Triggers**: Push to main, PRs to main, weekly (Sunday 00:00 UTC)

**Tool**: Lychee Link Checker v1.8.0

**Excluded URLs** (due to authentication, rate limiting, or privacy):
- `claude.ai/*` (authentication required)
- `reddit.com/*` (rate limiting)
- `linkedin.com/in/*` (profile privacy)
- `mondrian.dev/*` (temporary unreliable)
- Font CDNs, medical journals, specific pages

**Accepted Status Codes**: 200-308, 403, 429, 999

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

## Working with Experiments

The `/experiments/` directory hosts React/Vite applications alongside the main Jekyll site. These experiments are served as static SPAs at `https://humaine.studio/experiments/{experiment-name}/`.

### Experiments Structure
```
experiments/
└── {experiment-name}/
    ├── index.html           # Built Vite app entry point
    ├── .nojekyll            # REQUIRED: Prevents Jekyll processing
    ├── assets/
    │   ├── index-*.css      # Compiled CSS (hash-versioned)
    │   └── index-*.js       # Compiled JavaScript (hash-versioned)
    └── [other static files]
```

### Critical Rules for Experiments

1. **ALWAYS include `.nojekyll`** in each experiment directory
   - Without this file, GitHub Pages will process the experiment with Jekyll
   - This causes asset serving failures and broken paths
   - Place `.nojekyll` at the root of the experiment directory

2. **Only commit built files** to the experiments directory
   - Build your React/Vite app locally with `npm run build` or `vite build`
   - Commit only the `dist/` output (renamed to experiment name)
   - Do NOT commit `src/`, `node_modules/`, or development files

3. **Hash-based asset versioning**
   - Vite automatically generates hashed filenames: `index-CiAQKk_N.css`
   - This ensures cache busting when you deploy updates
   - Commit the entire `assets/` directory with each build

4. **Link to experiments from main site**
   - Add navigation links in appropriate pages
   - Example: `[Invoice Collaboration](/experiments/invoice-collab/)`
   - Document the experiment's purpose in the page that links to it

### Current Experiments

#### **invoice-collab**
- **Purpose**: Invoice collaboration features (experimental)
- **Tech Stack**: React, Vite
- **Status**: Active development
- **URL**: https://humaine.studio/experiments/invoice-collab/

### Adding a New Experiment

```bash
# 1. Build your React/Vite app locally
cd /path/to/your/app
npm run build

# 2. Copy dist output to experiments directory
cp -r dist/ /path/to/humaine-studio/experiments/new-experiment/

# 3. Add .nojekyll to prevent Jekyll processing
touch experiments/new-experiment/.nojekyll

# 4. Commit and push
git add experiments/new-experiment/
git commit -m "Add: new-experiment to experiments"
git push origin feature/new-experiment

# 5. Create PR and merge to deploy
```

## Published Content

### Blog Posts (6 total)
Current published posts in `_posts/` directory:

| Date | Title | Topics |
|------|-------|--------|
| 2021-02-20 | AI Inequality and the Digital Future of Work | AI ethics, automation, human dignity |
| 2024-08-10 | Connecting Claude to Notion with MCP | MCP, Claude, Notion integration |
| 2024-08-11 | Building Humaine Studio with Jekyll | Web development, Jekyll, site philosophy |
| 2025-08-18 | Gilfoyle | Claude agent development, automation |
| 2025-08-19 | LinkedIn Certifications: PostHog | PostHog analytics, certification |
| 2025-11-17 | Building Notion-Claude Code Auto-Sync | MCP automation, production workflows |

### Special Pages
Root-level pages served at `https://humaine.studio/{page-name}/`:

- **index.md** - Homepage with hero, philosophy, research areas, writing section
- **calculator.md** - T1D Insulin Calculator
  - Carb-to-insulin calculations (ICR)
  - Correction factor calculations (ISF)
  - localStorage for user settings
  - Multiple insulin types supported
  - Roadmap at `docs/calculator-roadmap.md`
- **posthog-cover-letter.md** - PostHog Technical Account Executive/Manager cover letter
- **privacy.md** - Privacy policy with PostHog/Apollo.io disclosure
- **weeks-of-life.html** - Interactive life weeks visualization

### Documentation Files
- **CLAUDE.md** - This file, loaded by Claude Code for context
- **llm.txt** - LLM optimization metadata (content hierarchy, technical stack)
- **SESSION_CONTEXT.md** - Ongoing development session notes
- **README.md** - Public project documentation
- **docs/calculator-roadmap.md** - T1D calculator feature roadmap (IOB, history, time-based ratios)

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

### Active External Integrations
```bash
# ✅ Currently Integrated
- PostHog Analytics (phc_gKgLr0iMjD1gnLV3yd8lEYWIUWmkIk8BuI6jUG3rTBg)
  - Privacy-focused analytics
  - person_profiles: 'identified_only'
  - Configured in _layouts/default.html
  - Privacy policy disclosure in privacy.md

- Apollo.io Visitor Intelligence (app_id: "68bb19f655bf65001d82c61f")
  - Company/visitor enrichment for job hunting
  - microTracker embedded inline
  - Privacy policy disclosure in privacy.md

- Google Fonts (Inter font family)
  - CDN: fonts.googleapis.com, fonts.gstatic.com

# ✅ Safe for static sites (examples)
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

## Known Issues & Future Improvements

### Active Issues
Based on workflow comments and repository state:

1. **Issue #19: Spell Check Wordlist Refinement**
   - Status: Non-blocking in CI (`continue-on-error: true`)
   - Action: Refine `.github/wordlist.txt` to reduce false positives
   - Impact: Currently allows merging with spell check failures

2. **Issue #20: Lighthouse CI 404 Errors**
   - Status: Non-blocking in CI (`continue-on-error: true`)
   - Action: Fix 404 errors before making Lighthouse checks blocking
   - Impact: Performance audits run but don't block merges

3. **Issue #22: UTF-8 Encoding in Jekyll Builds** (RESOLVED)
   - Solution: Set `LANG=C.UTF-8` in workflow
   - Status: Fixed in jekyll-checks.yml
   - Context: Prevented Jekyll build failures on special characters

### Planned Calculator Enhancements
From `docs/calculator-roadmap.md`:

- **Insulin on Board (IOB) Tracking** (CRITICAL for safety)
- Dose history logging
- Time-based ratios (different ICR/ISF by time of day)
- Data export for medical appointments

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
11. **ALWAYS include `.nojekyll`** in experiment directories - prevents Jekyll processing of React/Vite apps
12. **ALWAYS run `specstory sync --no-cloud-sync` at session end** - documents work history automatically
13. **Check active issues** - some CI checks are non-blocking (spell check, Lighthouse)
14. **Privacy disclosure** - any new tracking must be documented in privacy.md

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
- Blog posts: `_posts/YYYY-MM-DD-title.md`
- Pages: `page-name.md` (root level)
- Layouts: `_layouts/`
- Includes: `_includes/`
- Assets: `assets/css/`, `assets/js/`, `assets/images/`, `assets/resume/`
- Config: `_config.yml`
- CI/CD: `.github/workflows/`
- Testing configs: `.htmlhintrc`, `lighthouserc.js`, `.spellcheck.yml`
- Experiments: `experiments/{experiment-name}/` (React/Vite SPAs)
- Documentation: `docs/`, `CLAUDE.md`, `llm.txt`, `SESSION_CONTEXT.md`
- Session history: `.specstory/history/` (gitignored)

---

*This file is version-controlled and shared with the team. Update it as the project evolves.*