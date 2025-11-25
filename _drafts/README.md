# Drafts

Work-in-progress blog posts that are not yet published.

## How Drafts Work

Posts in this directory are **not published** to the live site. They exist only locally and in version control.

### Creating a Draft

```bash
# Create new draft
touch _drafts/your-post-title.md

# Add front matter
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD
categories: [category1, category2]
excerpt: "Brief description"
---
```

### Previewing Drafts

```bash
# Start Jekyll with drafts enabled
bundle exec jekyll serve --drafts

# Your draft will be visible at:
# http://localhost:4000/posts/.../your-post-title/
```

### Publishing a Draft

When ready to publish, move the draft to `_posts/` with a date prefix:

```bash
# Move to _posts with today's date
mv _drafts/your-post-title.md _posts/$(date +%Y-%m-%d)-your-post-title.md

# Commit and push
git add _posts/*.md
git commit -m "Publish: Your Post Title"
git push origin main
```

### Draft Workflow Tips

1. **Commit frequently** - Each commit is a save point
2. **Use descriptive commit messages** - "Draft: Added introduction section"
3. **Preview before publishing** - Always run `jekyll serve --drafts` first
4. **Update topics list** - Mark topic as "In Progress" when drafting

### Collaboration

If working with others, drafts in version control allow for:
- Review and feedback before publishing
- Collaborative editing
- Version history of writing process
