# Humaine Studio

A minimalist website for AI research focused on human-machine collaboration. Built on Jekyll with some help from Claude Code. 

## About

Humaine Studio is a thought lab exploring the intersection of artificial intelligence and human judgment. The site presents research on practical AI applications that augment rather than replace human decision-making.

Building this website was an experiment itself to demonstrate how someone can use tools like Claude Code and GitHub to build functional portfolio and blogging websites. 

## Features

- **Minimal Design**: Clean layout focused on content
- **Jekyll Blogging**: Full blog functionality with Markdown posts. https://jekyllrb.com/
- **GitHub Pages Ready**: Automated deployment with custom domain support
- **SEO Optimized**: Meta tags, structured data, and search engine friendly
- **Mobile Responsive**: Works well on all device sizes
- **AI Optimized**: Includes LLM.txt for better AI understanding

## Quick Start

1. Clone this repository
2. Install Jekyll: `gem install jekyll bundler`
3. Install dependencies: `bundle install`
4. Run locally: `bundle exec jekyll serve`
5. Visit `http://localhost:4000`

## Writing Blog Posts

Create new posts in the `_posts` directory using the format:
`YYYY-MM-DD-post-title.md`

Example front matter:
```yaml
---
layout: post
title: "Your Post Title"
date: 2024-08-11 12:00:00 -0500
categories: [category1, category2]
tags: [tag1, tag2]
excerpt: "Brief description of the post"
---
```

## Deployment

The site is configured for GitHub Pages with automatic deployment. Simply push to the main branch and GitHub will build and deploy the site.

For custom domain setup:
1. Add your domain to the `CNAME` file
2. Configure DNS settings with your domain provider
3. Enable GitHub Pages with custom domain in repository settings

## Configuration

Key settings in `_config.yml`:
- Site title and description
- Author information
- Social media links
- SEO settings

## File Structure

```
├── _config.yml          # Site configuration
├── _layouts/            # Page templates
├── _includes/           # Reusable components
├── _posts/              # Blog posts
├── assets/
│   ├── css/main.css     # Stylesheet
│   └── js/main.js       # JavaScript
├── index.md             # Homepage
├── robots.txt           # SEO file
├── llm.txt             # AI optimization
└── CNAME               # Custom domain
```
## Future Maybe Updates
- Look at a content management system like [SiteLeaf](https://www.siteleaf.com/) or [CloudCannon](https://cloudcannon.com/)

## License

This project is open source and available under the MIT License.

## Contact

Chris McConnell  
Email: chris@humaine.studio  
Website: https://humaine.studio
