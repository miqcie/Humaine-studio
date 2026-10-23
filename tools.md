---
layout: default
title: Tools
permalink: /tools/
description: "Tools and projects Chris McConnell built in 2025 and 2026: civic pages, AI agents and evals, data viz, compliance tooling and health tools. Each with what it is, how it was built, and what went wrong."
---

# Tools

Things I built in the last eighteen months, most of them with Claude Code. Each card says what it is, why it exists, how it was built and what went wrong. Code is on [GitHub](https://github.com/miqcie).

## Civic

### Notes From the Back Row

![Live notes page from the Chesterfield Planning Commission, Oct. 20, 2026](/assets/images/showcase/back-row.jpg)

**What is it:** A live, plain-English play-by-play of a county planning hearing, so neighbors can follow without sitting through four hours of video.

**Why does it exist:** Big votes happen late at night on a feed few people watch. I wanted neighbors to see what was said while it was said.

**What problem does it solve:** No more waiting days for minutes. Anyone with the link got easy-to-read, timestamped notes, right up to the 5-0 vote to delay.

**How was it built:** In one evening with Claude Code. I was sitting in the meeting room, and 30 minutes in I wanted to follow the questions behind the questions. My laptop pulled the county livestream, faster-whisper in Python transcribed it in 30-second clips, and a Claude artifact page updated all night.

**Mistakes and lessons:** YouTube blocked the cloud server as a bot, so the fix was my own laptop on a phone hotspot. Notes ran three minutes behind until I asked for 30-second clips, and went dark for four minutes when the laptop slept. Lessons: run `caffeinate` to keep the machine awake, keep the public feed apart from my private coaching, and let a friend proofread live (one caught a bug).

**Other applications:** School board nights, court hearings for families, union bargaining, shareholder meetings, disaster briefings in other languages, a private "subtext" feed for organizers.

[See it here](https://claude.ai/artifact/P3D41hHKumTk8MhzuVt1SJ)

### Two Clicks to City Hall

![Bon Air Speaks Up action page](/assets/images/showcase/bon-air.jpg)

**What is it:** A one-page kit that turns "I should say something" into a ready email to the county Planning Commission.

**Why does it exist:** Chesterfield's draft land plan capped Bon Air's village center at two stories, and comments closed in about a day.

**What problem does it solve:** Neighbors got a countdown, three clear asks, and plain notes they could edit and send, written at a 5th to 8th grade level.

**How was it built:** Overnight, Oct. 18 to 19, 2026, with Claude Code: plain HTML on a Cloudflare Worker, a QR flyer made in Python, and automated accessibility tests in light and dark at phone and desktop widths. Thirteen pull requests.

**Mistakes and lessons:** The brand-new domain would not resolve on my laptop, so the tests pointed the browser at it by hand. The tests caught two real bugs: text spilling over at 200% zoom and buttons a screen reader could not read. Lesson: under a deadline, plain HTML plus automated checks wins.

**Other applications:** School board fights, tenant associations, union contract votes, comments on federal rules, any deadline where the barrier is a blank page.

[See it here](https://bonairvillage.org) (the hearing was Oct. 20, 2026)

## Data and sites

### The Traffic Tax

![Richmond Rush-Hour Reach map](/assets/images/showcase/traffic-tax.jpg)

**What is it:** A price tag on traffic, shown for your own front door. It tells you how many jobs you lose every rush hour just because the roads are full.

**Why does it exist:** Traffic is a tax nobody votes on and nobody sees on a bill. Mercatus measured it for the whole country, and I wanted to make that hidden tax visible to the people who pay it.

**What problem does it solve:** We argue about roads, zoning and transit in the abstract. This turns "congestion" into a number you can feel: the jobs you can't reach from your street.

**How was it built:** In about a day with Claude Code: Mercatus commuter data and 2023 Census job counts for 353 Richmond neighborhoods, one D3 web page for the map, and OpenStreetMap for address search.

**Mistakes and lessons:** The build workspace could not reach the address-search service, so I tested it against stand-ins. Lesson: when you can't test the real thing, fake it on purpose and say so.

**Other applications:** Wage bargaining, home listings, remote-work policy, parole job conditions, bridge-closure planning, any public dataset made personal by street address.

[See it here](https://cmm.dev/viz/richmond-rush-hour-reach/)

### A 1987 Mac for 2026 Robots

![cmm.dev styled as a 1987 Macintosh desktop](/assets/images/showcase/cmm-dev.jpg)

**What is it:** My personal site, dressed as a black-and-white 1987 Macintosh, built so AI agents can read it as easily as people.

**Why does it exist:** The first version drew text with code at pixel positions, so machines saw nothing. An agent-readiness check scored it 4 out of 100.

**What problem does it solve:** Every word is now plain HTML that works with JavaScript off, plus a summary file for AI. The score went to 100.

**How was it built:** Vite and TypeScript on a Cloudflare Worker with Claude Code, March to October 2026, 19 pull requests and 28 tests. It also holds my data viz shelf.

**Mistakes and lessons:** A Cloudflare bot blocker was turning away every agent; switching it off alone moved the score from 5 to 93. A rescan showed an old cached score until I waited. A design review caught four overlapping-window bugs the build missed. Lesson: check what the robots actually see.

**Other applications:** City services pages, library catalogs, job postings, restaurant menus, product pages.

[See it here](https://cmm.dev)

### Mapping the First Mile

![Eagle Ridge CMMC market map](/assets/images/showcase/market-map.jpg)

**What is it:** The site for my CMMC readiness practice, with a map of 89 firms that serve defense contractors, and the gap where small suppliers fall through.

**Why does it exist:** Small defense suppliers must pass a cybersecurity audit, and almost nobody helps them before the assessor arrives. The map made that gap visible.

**What problem does it solve:** A small contractor sees the whole market on one screen, in 13 categories, with sources.

**How was it built:** Astro on Cloudflare with Claude Code, rebuilt in one session in June 2026 to Lighthouse scores of 99 to 100. 92 pull requests over a year. The practice wound down in September 2026.

**Mistakes and lessons:** One deploy said "Active" but served 404s on every page, so now I check the live site after each deploy. Moving the domain cost ten minutes of downtime until I removed old records first. An early entry misstated a competitor's prices; I fixed it after publishing. Lesson: a push is not a deploy.

**Other applications:** Legal aid gaps, childcare deserts, rural health services, startup ecosystems, any market a newcomer can't see.

[See it here](https://eagleridge.io/market-map)

## Agents and evals

### Grading the Robot Assessor

![Heatmap of nine AI models scored across 36 CMMC assessor tasks](/assets/images/showcase/optima.jpg)

**What is it:** A 36-question exam that tests whether AI models can think like a CMMC assessor, graded on 1,027 points.

**Why does it exist:** Contractors are starting to use AI for compliance paperwork, but no public test checked the judgment calls assessors make. The closest one only matched keywords.

**What problem does it solve:** Picking a model stops being guesswork. Of nine models, the top scored 90%, and one costing less than 1% of the priciest Claude run scored 80%.

**How was it built:** Python scripts build the tasks from anonymized case files, and Artificial Analysis Optima runs and grades them. Drafted in September, run Oct. 15, 2026.

**Mistakes and lessons:** My first tasks leaked their own answers, so I wrote drafting rules. The September files sat in a scratch folder that got wiped; I rebuilt them from the session log and matched the old numbers. Lesson: test the test, and keep work in a repo from day one.

**Other applications:** Auditor hiring screens, paralegal AI checks, insurance underwriting, grant review, procurement model picks.

[See it here](https://github.com/miqcie/optima-cmmc-assessor-judgment)

### The Grumpy Reviewer

![Gilfoyle repository on GitHub](/assets/images/showcase/gilfoyle.jpg)

**What is it:** A code reviewer with a dry wit that must quote the line behind every complaint, or drop it.

**Why does it exist:** AI reviewers pad reports with invented problems. I wanted one that says "ship it" when a change is clean. It began as a 2025 [joke post](/posts/2025/08/18/gilfoyle/) about the Silicon Valley character.

**What problem does it solve:** Before a push, one command answers ship or fix, and every piece of evidence is checked against the real files.

**How was it built:** Python and Claude Code. One source file builds versions for Claude Code, Codex, Cursor and Hermes. Rewritten in June 2026, 1.0 shipped Sept. 9. 14 pull requests, 40 tests, 29 GitHub stars.

**Mistakes and lessons:** A one-word test call cost 518,000 tokens because every global tool loaded, so isolation is now required. My first paid eval run saved only totals, so now each case is recorded as it finishes. Lesson: measure the measuring.

**Other applications:** Contract redlines, grant applications, building permits, lab notebooks, any review that should cite its source.

[See it here](https://github.com/miqcie/gilfoyle)

### The Economical Editor

![Deirdre repository on GitHub](/assets/images/showcase/deirdre.jpg)

**What is it:** An editor in a box. It reads your draft by Deirdre McCloskey's rules and offers a rewrite for every fault.

**Why does it exist:** Everything I drafted with AI sounded like AI. Claude pointed me to McCloskey's *Economical Writing*, and I turned its rules into a checklist. An homage, not affiliated. The [story is here](/posts/2026/09/28/i-hired-deirdre-mccloskey-to-edit-my-writing/).

**What problem does it solve:** Writers get specific fixes instead of vague advice, plus a quick check that flags 20 common AI tells before a commit.

**How was it built:** A Claude Code skill and agent written in Markdown, plus a small Bash and Perl linter. First version in August 2026; public plugin and v2.1 on Sept. 28.

**Mistakes and lessons:** Deirdre reviewed her own README and caught an install step that broke the skill. The linter flagged the README's own examples, so it now skips quotes and code. Plugin versions drifted, so one release script now bumps them together. Lesson: point the tool at itself first.

**Other applications:** Grant writing, legal briefs, policy memos, ESL coaching, product docs, cover letters.

[See it here](https://github.com/miqcie/deirdre)

### Half the Rules, Same Results

![Config trim A/B results page](/assets/images/showcase/config-trim.jpg)

**What is it:** A test bench that proves you can cut half the standing instructions you give an AI coding helper without making it worse.

**Why does it exist:** My setup loaded about 12,000 tokens of rules every session, and some contradicted each other. Anthropic said it cut most of its own prompt with no loss; I wanted proof for mine.

**What problem does it solve:** You trim on evidence, not a hunch: the same tasks, old setup against new, pass rate and cost side by side. Mine fell to about 6,000 tokens, passed as well, and ran 10 to 15% cheaper.

**How was it built:** Bash, jq and Python driving Claude Code, over three days in July 2026, with a [results page](/config-trim-results.html) and a [write-up](/posts/2026/07/31/i-deleted-half-my-claude-config/) on this site.

**Mistakes and lessons:** Four of seven flagged failures were bugs in my own check scripts. One check passed on code nobody touched, and a label swap flipped the verdict. Lesson: audit the judge before the defendant.

**Other applications:** Employee handbooks, compliance policies, hospital checklists, legal boilerplate, onboarding docs.

[See it here](https://github.com/miqcie/claude-config-evals)

### The Free Booking Bridge

![cal-attio val on Val Town](/assets/images/showcase/cal-attio.jpg)

**What is it:** Every meeting someone books on my calendar lands in my customer list on its own, cancellations and reschedules included.

**Why does it exist:** I was paying a service for this sync. The data already moved by webhook; it only needed a small, free bridge.

**What problem does it solve:** No copying bookings by hand and no monthly fee.

**How was it built:** TypeScript on Val Town with Claude Code, checking each message's signature. Six pull requests in about 90 minutes on July 6, 2026, then tested with real bookings.

**Mistakes and lessons:** Real cancellations sent an empty field my test samples left out, and the CRM rejected them, though 18 tests were green. A repeat customer's second booking overwrote the first until I looked bookings up by ID. The free CRM plan blocked new record types, so bookings became a list. Lesson: test with real data early.

**Other applications:** Clinic intake, tutoring schedules, court-date tracking, volunteer shifts, any paid connector that is really a webhook.

[See it here](https://github.com/miqcie/cal-attio-sync) or [on Val Town](https://www.val.town/x/miqcie/cal-attio)

### Nothing Gets Lost

**What is it:** A nightly backup of every conversation I have with AI coding tools, with one search box across all of them.

**Why does it exist:** I found my 2025 Mondrian build sessions gone. Claude Code deletes old logs after 30 days by default, and I had no backup.

**What problem does it solve:** Every session from every tool is kept, encrypted and searchable. I recovered the lost build from older notes.

**How was it built:** Bash, macOS launchd, restic to Amazon S3, and Python with SQLite search, over five days in September 2026. The first backup took 24 minutes for 10 GB; now it takes about a minute a night.

**Mistakes and lessons:** macOS still ships a 2007 Bash that broke on empty lists. My first design named tools one by one and missed two thirds of sessions, as Gilfoyle pointed out; now it backs up everything unless excluded. Lesson: opt out beats opt in.

**Other applications:** Lab notebooks, legal holds, newsroom source logs, classroom records.

The code is private.

## Compliance

### A Referee for AI Paperwork

![Eagle Ridge methodology docs site](/assets/images/showcase/cmmc-docs.jpg)

**What is it:** Nine AI helpers that walk a small defense contractor through CMMC prep, with 340 automatic checks on their work.

**Why does it exist:** Compliance documents go straight to an auditor, and one wrong number becomes a finding. AI writing needed a referee.

**What problem does it solve:** The scoring math, which gaps may wait for a later fix, and client-specific wording are all checked before a person signs off.

**How was it built:** Python, pytest and Claude Code agents, February to September 2026. The first eight agents shipped in one session. 69 merged pull requests.

**Mistakes and lessons:** The tests caught 16 controls with the wrong point values, so a plan to defer them would have failed the audit. A real engagement showed my proposal wording blurred the scope, so I added an intake checklist. Lesson: tests find the expensive mistakes.

**Other applications:** Tax preparation, building inspections, grant compliance, clinical-trial paperwork, HR policy audits.

[See it here](https://docs.eagleridge.io) (public method docs; the code is private)

## Health and time

### Glucose at a Glance

![Nightscout clock web flasher](/assets/images/showcase/nightscout-clock.jpg)

**What is it:** A small pixel clock that shows a child's blood sugar from their glucose monitor, set up by a parent with no code.

**Why does it exist:** The open-source clock worked but was built for developers: config files and IP addresses. Parents need an appliance.

**What problem does it solve:** Flash it from a web page, join the clock's Wi-Fi, pick your monitor, set a PIN. Done.

**How was it built:** C++ on an ESP32 with PlatformIO, a browser flasher on GitHub Pages, and Claude Code. It sits on Artiom Kenibasov's firmware; my 42 commits add the setup layer. Twelve pull requests in one session, then flashed on a real clock.

**Mistakes and lessons:** Scanning for Wi-Fi froze the setup page, so the scan now runs once at boot. Safari blocked plain links to local devices, so setup became one page. The USB chip failed a third of flashes until I slowed it down. Lesson: real hardware tells the truth.

**Other applications:** Elder care, oxygen or CPAP alerts, pool and plant sensors, shop-floor counters, any number a family needs at a glance.

[See it here](https://miqcie.github.io/nightscout-clock/) (not a medical device)

### Show Your Math

![T1D insulin calculator](/assets/images/showcase/calculator.jpg)

**What is it:** A calculator that shows each step of a mealtime insulin estimate, so you can follow the math instead of trusting it. Educational, not medical advice.

**Why does it exist:** The math is simple but easy to fumble at the table, and most apps hide it.

**What problem does it solve:** You see each number and its source, switch units, and keep your settings in your own browser.

**How was it built:** Plain JavaScript on this Jekyll site with tests, launched October 2025. A SwiftUI iPhone version is in progress.

**Mistakes and lessons:** For months the sliders showed different numbers on load than the math used; one shared default fixed it, with tests that fail on the old code. A review found the iPhone version skipped range checks, now enforced. The top safety feature on the roadmap, insulin on board, is not built yet. Lesson: what you show must be what you compute.

**Other applications:** Nursing school drills, loan payoff, recipe scaling, tax estimates, any formula people should see.

[See it here](/calculator/)

### Your Life in Weeks

![Life in weeks grid](/assets/images/showcase/weeks-of-life.jpg)

**What is it:** Type your birthday and see your whole life as a grid of weeks, with the ones behind you filled in.

**Why does it exist:** Tim Urban and Oliver Burkeman showed how short and finite a life is. I wanted a version anyone could open.

**What problem does it solve:** A big abstract number becomes a picture you can't unsee, with stats on time, people and the cosmos.

**How was it built:** It started as a React artifact in Claude.ai, then became a single page on this site with Claude Code in August 2025.

**Mistakes and lessons:** None recorded for this one-day port.

**Other applications:** Retirement planning, hospice conversations, teen money lessons, parental-leave policy, project deadlines counted in weeks.

[See it here](/weeks-of-life/)

## Archived

### Proof, Not Screenshots

![Mondrian weekend build post](/assets/images/showcase/mondrian.jpg)

**What is it:** A tool that blocks risky cloud changes and signs a receipt proving the check ran. Archived.

**Why does it exist:** Startups lose deals without security certificates, and the proof is often a screenshot. I built it during Startup Virginia's Idea Factory.

**What problem does it solve:** An auditor would get a signed record instead of a picture.

**How was it built:** Go and GitHub Actions with Claude Code, in about four hours on Sept. 13, 2025. Archived in January 2026.

**Mistakes and lessons:** The GitHub Action took several rounds of shell fixes. The bigger mistake: I wrote code before talking to buyers, then learned existing tools covered most of the job. Lesson: interviews before code.

**Other applications:** Food-safety logs, chain of custody for evidence, drug-trial records, election audits.

[See it here](/posts/2026/01/11/experiments-building-grc-tool-weekend/)

## Smaller builds

- [usaspending-mcp-server](https://github.com/miqcie/usaspending-mcp-server): lets an AI assistant search federal contract awards in plain language. Sixteen read-only tools; the docs are still a draft.
- [grepai-beads-helpers](https://github.com/miqcie/grepai-beads-helpers): one-command setup for local code search and agent memory.

## How this page was made

### The Showcase Writer

**What is it:** The recipe behind this page: a short skill that turns a finished project into a card anyone can read in a minute.

**Why does it exist:** My work was scattered across 31 repos, chat logs and live sites, and most of it never got written up. A resume can't show what a build taught me.

**What problem does it solve:** Every project answers the same eight questions, facts only, so you can compare them side by side.

**How was it built:** A Claude Code skill in one Markdown file. For this page, research agents swept my repos, build notes, memory files and live sites, then Claude drafted each card to match two I wrote by hand. One afternoon, Oct. 23, 2026.

**Mistakes and lessons:** The first sweep missed many of my commits because I sign some as "Human." One "build" was an untouched template and one repo was someone else's fork, so both were cut. Lesson: an evidence sweep is only as good as its filters.

**Other applications:** Grant reports, performance reviews, case studies, lab write-ups, nonprofit annual reports.
