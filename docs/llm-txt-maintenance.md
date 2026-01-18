# llm.txt Maintenance Guide

## What is llm.txt?

`llm.txt` is a standardized file that helps AI models (like Claude, ChatGPT, Perplexity) understand your website's content, structure, and purpose. It's served at `https://humaine.studio/llm.txt` and acts like a comprehensive README specifically for LLMs.

## When to Update llm.txt

Update the file whenever you make these changes:

### ✅ MUST Update
- **Add/remove blog post** → Update "Blog Posts" section with count and new entry
- **Add/remove primary page** → Update "Primary Pages" section
- **Add/remove experiment** → Update "Experiments" section
- **Major tech stack change** → Update "Technical Stack" section
- **Change site purpose/positioning** → Update "Site Overview" section

### 📝 SHOULD Update
- **Update PostHog/analytics setup** → Update "Analytics & Tracking"
- **Add new CI/CD workflow** → Update "CI/CD Pipeline"
- **Change site philosophy/focus** → Update "Core Philosophy" and "Key Messages"
- **Update contact methods** → Update "Contact & Collaboration"

### ⚪ Optional Update
- **Minor CSS/styling changes** → Usually not needed
- **Typo fixes in posts** → Not needed
- **Image additions** → Not needed unless it's a new feature

## Update Checklist

When updating llm.txt:

1. **Update the content sections**
   - [ ] Verify blog post count matches `_posts/` directory
   - [ ] Add new posts with date and topics
   - [ ] Update primary pages if added/removed
   - [ ] Update experiments if added/removed

2. **Update metadata**
   - [ ] Change "Last Updated" date to current date
   - [ ] Review "Site Overview" for accuracy
   - [ ] Check "Author Information" is current

3. **Update technical details**
   - [ ] Verify tech stack is accurate
   - [ ] Update CI/CD pipeline if workflows changed
   - [ ] Check analytics configuration

4. **Commit with clear message**
   ```bash
   git add llm.txt
   git commit -m "Update: llm.txt with [what changed]"
   ```

## Quick Update Commands

```bash
# Check blog post count (should match llm.txt)
ls -1 _posts/*.md | wc -l

# Check last modified date of llm.txt
grep "Last Updated" llm.txt

# List all root-level pages
ls -1 *.md *.html | grep -v README

# List experiments
ls -1 experiments/
```

## Integration with CLAUDE.md

When updating CLAUDE.md, ask yourself:
- Does this change affect site structure, content, or purpose?
- If yes → update llm.txt as well
- Both files should tell consistent stories, but:
  - **CLAUDE.md** = Instructions for Claude Code (how to work on the project)
  - **llm.txt** = Information for all LLMs (what the site contains)

## Automation Opportunities

Consider these future enhancements:

1. **Script to auto-count content**
   ```bash
   # scripts/check-llm-txt.sh
   POST_COUNT=$(ls -1 _posts/*.md | wc -l)
   LLMTXT_COUNT=$(grep -c "^[0-9]\." llm.txt)
   if [ $POST_COUNT -ne $LLMTXT_COUNT ]; then
     echo "⚠️  llm.txt may be out of sync"
   fi
   ```

2. **Pre-commit hook** to remind about llm.txt updates

3. **GitHub Action** to auto-update "Last Updated" date

## Verifying LLM Discovery

### How llm.txt Works

`llm.txt` is a **convention**, not a web standard. It's inspired by `robots.txt` and `humans.txt`. LLMs that support it will:
1. Check for the file at `https://yourdomain.com/llm.txt`
2. Read and parse the content
3. Use it to better understand your site when answering questions

**Important:** Not all LLMs automatically check for llm.txt. It's an emerging convention.

### Testing File Accessibility

1. **Manual URL Test (Most Important)**
   ```bash
   # After deploying, verify the file is publicly accessible
   curl https://humaine.studio/llm.txt

   # Or just open in browser:
   # https://humaine.studio/llm.txt
   ```

   ✅ **Expected result:** Should see your llm.txt content as plain text
   ❌ **If 404 error:** File not being served by Jekyll/GitHub Pages

2. **Check Jekyll Build**
   ```bash
   # Build locally and check output
   bundle exec jekyll build
   ls -la _site/llm.txt

   # Preview locally
   bundle exec jekyll serve
   # Then visit: http://localhost:4000/llm.txt
   ```

3. **Verify in GitHub Pages**
   - Go to repository Settings → Pages
   - Confirm site is published
   - Click "Visit site" → manually append `/llm.txt` to URL

### Testing with LLMs

Once your file is accessible, test if LLMs can find and use it:

#### Test with Claude (claude.ai or Claude Code)
```
Prompt: "Can you read the llm.txt file from humaine.studio and tell me what you learned about the site?"
```

Expected: Claude should fetch the URL and summarize the content.

#### Test with Perplexity
```
Prompt: "Look at humaine.studio's llm.txt file and describe what the site is about"
```

Perplexity has web access and should be able to fetch public URLs.

#### Test with ChatGPT (with browsing enabled)
```
Prompt: "Visit https://humaine.studio/llm.txt and summarize what this site offers"
```

Note: ChatGPT requires explicit URL mention to fetch content.

### Common Issues & Fixes

**Problem: llm.txt returns 404**
- **Cause:** File in wrong location or Jekyll not copying it
- **Fix:** Ensure file is at repository root (not in subdirectory)
- **Jekyll note:** Files at root are automatically copied to `_site/` unless excluded in `_config.yml`

**Problem: llm.txt shows as HTML instead of plain text**
- **Cause:** Jekyll is processing it as markdown/template
- **Fix:** Add to `_config.yml` under `include:` to copy as-is:
  ```yaml
  include:
    - llm.txt
  ```

**Problem: LLM says "I can't access external URLs"**
- **Cause:** Some LLMs don't have web browsing enabled
- **Fix:** Copy/paste the llm.txt content directly into the conversation

**Problem: LLM doesn't find useful info**
- **Cause:** LLM may not automatically check for llm.txt
- **Fix:** Explicitly mention the file: "Check the llm.txt file at humaine.studio"

### Monitoring Discovery

```bash
# Check if llm.txt is being accessed (if you have analytics)
# PostHog query: Filter events for URL path = "/llm.txt"

# Check GitHub Pages build logs
gh run list --workflow=jekyll.yml --limit 1
gh run view [run-id] --log

# Verify file in deployed site
wget https://humaine.studio/llm.txt -O -
```

### Best Practices for Discoverability

1. **Keep file at root** - `https://humaine.studio/llm.txt` (not in subdirectory)
2. **Use plain text markdown** - No fancy formatting that breaks parsing
3. **Update regularly** - Stale info is worse than no info
4. **Link to it** - Mention in footer or about page for humans to discover too
5. **Test after every deploy** - Quick curl check to ensure it's still accessible

### Example: Adding a link in your footer

You could add this to `_includes/footer.html`:
```html
<a href="/llm.txt" title="Machine-readable site information">llm.txt</a>
```

This makes it discoverable by humans too!

---

*Last Updated: 2026-01-18*
