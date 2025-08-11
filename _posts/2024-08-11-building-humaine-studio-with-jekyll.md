---
layout: post
title: "Building Humaine Studio: A Jekyll Website for AI Research"
date: 2024-08-11 12:00:00 -0500
categories: [web development, jekyll, ai research]
tags: [jekyll, github pages, web design, portfolio]
excerpt: "How I built a minimalist research portfolio website using Jekyll, focusing on clean design and effective presentation of AI research work."
---

Building a research portfolio website requires balancing simplicity with functionality. For Humaine Studio, I wanted something that felt professional, loaded quickly, and could grow with my research work. After considering various options, I chose Jekyll for its simplicity and GitHub Pages integration.

## Design Philosophy

I drew inspiration from Sam Altman's website—clean, minimal, and focused on content rather than flashy design. The goal was to create something that felt professional without being overwhelming, letting the research and writing speak for itself.

Key design principles:
- **Minimal and clean**: White background, plenty of whitespace, clean typography
- **Content-focused**: Clear hierarchy that guides readers through different sections
- **Fast loading**: No heavy frameworks or unnecessary JavaScript
- **Mobile responsive**: Works well on all device sizes

## Technical Choices

### Jekyll + GitHub Pages

Jekyll was the natural choice for several reasons:
- Static site generation for fast loading
- Built-in blog functionality
- GitHub Pages integration for easy deployment
- Markdown support for easy writing
- No database or server management required

### Typography and Layout

I chose Inter as the primary font—it's clean, readable, and works well at different sizes. The layout uses a centered container with a max-width of 800px, creating comfortable reading lines and plenty of whitespace.

The homepage is structured as a single page with multiple sections:
- Hero section with name and brief introduction
- Philosophy section explaining my approach to AI research
- Research areas outlining key focus areas
- Writing section showing recent blog posts
- Contact information

## Jekyll Structure

The site follows standard Jekyll conventions:

```
├── _config.yml          # Site configuration
├── _layouts/            # Page templates
│   ├── default.html     # Base layout
│   ├── home.html        # Homepage layout
│   └── post.html        # Blog post layout
├── _posts/              # Blog posts
├── assets/
│   ├── css/
│   └── js/
├── index.md             # Homepage content
└── Gemfile              # Ruby dependencies
```

### Configuration

The `_config.yml` file sets up the site for GitHub Pages deployment with SEO optimization:

```yaml
title: Humaine Studio
description: "A thought lab exploring human-machine collaboration..."
url: "https://humaine.studio"

plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag
```

### Custom Layouts

I created three main layouts:

1. **Default layout** (`default.html`): The base template with navigation, header, and footer
2. **Home layout** (`home.html`): Extends default for the homepage
3. **Post layout** (`post.html`): For individual blog posts with navigation between posts

## CSS Architecture

The CSS is organized in a single file for simplicity, with clear sections:

- Reset and base styles
- Layout components (container, header, footer)
- Section-specific styles (hero, research, writing)
- Blog post styles
- Responsive design

I used CSS custom properties for colors and made heavy use of flexbox for layout. The design is mobile-first with progressive enhancement for larger screens.

## Blog Integration

Blog posts live in the `_posts` directory following Jekyll's naming convention: `YYYY-MM-DD-title.md`. The homepage automatically pulls in recent posts and displays them in the writing section.

Each post includes front matter for metadata:

```yaml
---
layout: post
title: "Post Title"
date: 2024-08-11 12:00:00 -0500
categories: [category1, category2]
tags: [tag1, tag2]
excerpt: "Brief description..."
---
```

## SEO and Performance

The site includes several optimization features:

- Jekyll SEO plugin for meta tags
- Semantic HTML structure
- Fast loading with minimal CSS/JS
- Responsive images
- Clean URLs
- Sitemap generation

## Deployment Process

The deployment process is streamlined:

1. Write posts in Markdown
2. Commit changes to GitHub
3. GitHub Pages automatically builds and deploys the site

This workflow makes it easy to publish new content without worrying about server management or build processes.

## Future Enhancements

Some features I'm considering for future updates:

- Search functionality for blog posts
- RSS feed styling
- Dark mode toggle
- Better syntax highlighting for code blocks
- Integration with research databases

## Conclusion

Jekyll proved to be an excellent choice for this research portfolio. It strikes the right balance between simplicity and functionality, allowing me to focus on content while maintaining a professional web presence. The GitHub Pages integration makes deployment seamless, and the Markdown-based workflow fits naturally with my research writing process.

The minimalist design philosophy serves the site's purpose well—presenting research and ideas clearly without unnecessary distractions. Sometimes the best technology choices are the ones that get out of the way and let you focus on what matters most.