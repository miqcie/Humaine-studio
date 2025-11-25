# Scripts

Helper scripts to streamline publishing workflows.

## mirror-to-substack.sh

Reduces friction when mirroring Jekyll posts to Substack.

**What it does:**
- Opens your published Jekyll post (to copy content)
- Opens Substack editor (to paste and publish)
- Displays a checklist of steps to complete
- Shows the canonical URL to copy

**Usage:**
```bash
./scripts/mirror-to-substack.sh "https://humaine.studio/posts/2025/11/25/post-title/"
```

**Why this helps:**
- Eliminates "what was that URL again?" moments
- Provides a checklist to ensure you don't forget the canonical URL
- Opens everything in the right order
- ADHD-friendly: clear steps, no guessing

## Future Scripts

Ideas for additional automation:
- `create-draft.sh` - Quick draft creation with template
- `publish-post.sh` - Move draft to _posts with date prefix
- `batch-social.sh` - Generate social media posts from published content
