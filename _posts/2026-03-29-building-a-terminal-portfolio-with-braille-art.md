---
layout: post
title: "Building a Terminal Portfolio with Braille Art and Zero Traditional Engineering"
date: 2026-03-29 16:00:00 -0400
categories: ["web development", "ai research", "claude code"]
tags: ["projects", "gridland", "terminal ui", "braille art", "cloudflare", "portfolio", "Claude Code"]
excerpt: "I built a terminal-style portfolio site that renders React on Canvas, converts my face into Unicode braille dots, and deploys to Cloudflare Pages. I'm not an engineer. Here's what happened."
---

I've been circling the "build a personal site" problem for months. The usual options felt wrong — a WordPress template, a Tailwind landing page, another static site that looks like every other static site. None of it matched the thing I actually wanted to project: that I build tools, not just talk about building them.

Then I found [gridland](https://github.com/thoughtfulllc/gridland).

## What gridland does

Gridland renders React components as a terminal UI on an HTML5 Canvas. Not a terminal emulator — actual React with JSX, but instead of DOM elements you get `<box>`, `<text>`, and `<span>` rendered as monospace characters on a canvas. It looks like you're SSHing into someone's server, but it's a website.

The real thing is at [cmm.dev](https://cmm.dev). Press `p` for projects, `a` for about, `h` to go home. Keyboard navigation, like a real terminal.

## The "Practitioner Who Builds" problem

Here's the thing. The original plan file — written in an earlier Claude Code session — described me as delivering "staff-level engineering with a bias toward shipping."

I am not a staff engineer. I have never been a traditional engineer. I have an English degree from the University of Idaho and an MBA from NYU Stern. My career path runs through legislative affairs, digital PR, luxury menswear, and field organizing before landing in cybersecurity compliance.

What I *am* is someone who learned to build through practice. I run [Eagle Ridge Advisory](https://eagleridge.io), where I do CMMC compliance consulting for defense contractors. I write the automation, not just the policy. I built the [methodology repo](https://github.com/miqcie/eagle-ridge-methodology), the SPRS calculators, the SSP generators, the control registers. I write Python, Go, Swift, TypeScript, and Shell — not because I went to school for it, but because the tools I needed didn't exist.

So the tagline became **"Practitioner Who Builds"** — which is the honest version of what I do.

## The braille portrait rabbit hole

I wanted a portrait on the About page. A photo wouldn't work — gridland renders to canvas, not DOM. Everything is monospace text. So: ASCII art.

The journey went like this:

**Attempt 1: jp2a with standard characters** (`#`, `%`, `@`, `*`, `+`). Unreadable. On a monospace grid, every character occupies the same space, so there's no tonal range. `@` and `.` are the same width. You get a wall of noise.

**Attempt 2: jp2a with the default charset** (`W`, `N`, `K`, `x`, `o`, `l`, `:`). Better — these characters have genuine visual weight differences. You could see a face at 35 characters wide. But it still felt like looking at a CAPTCHA.

**Attempt 3: chafa with braille characters**. This is where it got interesting.

Unicode braille characters (`⠀`, `⠁`, `⠂`, all the way to `⣿`) are each a 2×4 dot grid. That's 8 "pixels" per character cell, compared to 1 for traditional ASCII art. Eight times the resolution in the same space.

But my headshot had a gilt picture frame moulding behind me that created background noise. The conversion picked up the moulding's edges and turned them into dots.

**Attempt 4: rembg background removal + braille**. Ran the photo through [rembg](https://github.com/danielgatis/rembg) to strip the background, then converted. Cleaner, but a photograph has too much tonal ambiguity for braille to handle well. Skin gradients, fabric textures — they all become noise.

**Attempt 5: minimalist icon + braille**. The answer. I had a bold black-and-white illustrated portrait in my Caldris brand kit — clean lines, high contrast, no gradients. Fed it through chafa and got a crisp, immediately recognizable braille portrait. Bald head, glasses, beard, smile — all readable in about 28×14 characters.

The lesson: the source image matters more than the conversion. Clean line art converts to braille perfectly. Noisy photos don't.

## What broke along the way

Gridland is new software, and I ran into two framework-level issues that I filed upstream:

**[Issue #38](https://github.com/thoughtfulllc/gridland/issues/38): No JSX type declarations.** Gridland doesn't ship TypeScript types for its custom elements. Worse, some of its element names (`text`, `span`, `a`) collide with React 19's built-in types. The result: 48 TypeScript errors on a clean project. Vite compiles fine because it doesn't type-check, but `tsc` refuses. I wrote a local `.d.ts` as a workaround and filed the issue.

**[Issue #39](https://github.com/thoughtfulllc/gridland/issues/39): Top-level await breaks production builds.** Gridland bundles `yoga-layout` (Facebook's flexbox engine), which uses top-level `await`. Vite's default browser targets don't support it. The fix is one line in `vite.config.ts` (`build.target: "esnext"`), but you'd never know that without reading the error trace. The gridland vite plugin should set this automatically.

## Deploying to Cloudflare Pages

I compared GitHub Pages, Vercel, Cloudflare Pages, and Netlify. The real tradeoff: GitHub Pages requires you to maintain a deploy workflow but adds no new vendor. The other three are "connect repo and forget" but add another service.

I picked Cloudflare Pages as a deliberate stepping stone. Free static hosting now. But if the [GRC platform](https://github.com/miqcie/eagle-ridge-methodology/blob/main/docs/specs/2026-03-18-grc-platform-mvp-design.md) I'm building with [Talha](https://www.linkedin.com/in/talha-ansari/) needs Workers, KV storage, or a WAF later — it's already there. No migration, just turn things on.

The deploy chain:
1. `wrangler pages deploy dist` pushes the built site
2. GitHub Actions auto-deploys on every push to main
3. Porkbun nameservers pointed to Cloudflare
4. Custom domain verified, SSL auto-provisioned

The email DNS (MX records, SPF, DKIM, DMARC) survived the nameserver migration intact — which was the part I was actually nervous about.

## What I learned

Building this portfolio was a test of something I've been thinking about since the Gilfoyle conversation: the line between "real developer" and "person who builds things" is increasingly irrelevant. I used Claude Code for the implementation, chafa and rembg for image processing, and wrangler for deployment. The decisions — what framework, what copy, what architecture, how to handle the type system conflicts, where to host — those were mine.

The tools amplify what you already know. They don't replace the judgment calls. An English degree and an MBA aren't handicaps when you're building a compliance consulting business that happens to ship code. They're context.

The site is live at [cmm.dev](https://cmm.dev). The full build log is in the [repo](https://github.com/miqcie/Cmm.dev/blob/main/docs/BUILD_LOG.md).
