---
layout: home
title: "Humaine Studio"
description: "Applied AI explorations that keep humans in command. Safe, steerable use cases. Transparent workflows. Augmentation over replacement."
permalink: /
---

<div class="hero">
  <h1 class="hero-title">Chris McConnell</h1>
  <p class="hero-subtitle">Applied AI for human-machine collaboration.</p>
  <p class="hero-description">
  Humaine Studio explores how AI augments human capability. The work is grounded in Zero Trust security and clean, reliable data, focusing on safe, steerable use cases and transparent workflows that keep people in command.
</p>
</div>

<section id="philosophy" class="section">
  <h2 class="section-title">Philosophy</h2>
  <div class="section-content">
    <p>The optimistic view of AI sees two challenges to meet: building systems that approach aspects of human intelligence, and ensuring those systems expand rather than erode our capabilities.</p>
    <p>I focus on the “missing middle”: systems that help us think better without taking decisions away. The goal is oversight and augmentation, not replacement. That means building tools that teach as they assist, leaving people more capable than when they started.</p>
    <p>Augmentation only works if the systems we connect to are trustworthy. My background in Zero Trust security informs everything here—permissions are explicit, access is scoped, and actions are auditable. Clean, well-structured data is just as critical; without it, even the best AI workflows produce noise instead of insight.</p>
    <p>Leadership itself will change as organizations manage not only people but also teams of AI agents. Drawing on the Nadler–Tushman Congruence Model, I see future leaders needing both engineering fluency to direct autonomous systems and the judgment to lead the people who remain. The ability to align strategy, work, culture, and technology will be a defining skill for executives in an AI-driven organization.</p>
    <p>AI development and automation should follow the principles of humanistic design: dignity first, transparency always, and productivity that strengthens rather than strips away the human element. AI-enabled workflow automation should target the dumb, dirty, dangerous, and tedious work—freeing humans to tackle bigger problems and more creative pursuits. This has been the promise since the first industrial revolution, which raised living standards and expanded our economy. The future must ensure new work is meaningful, sustainable, and accessible; automation that strips people of purpose or dignity is a design failure.</p>
  </div>
</section>

<section id="research" class="section">
  <h2 class="section-title">Research Areas</h2>
  <div class="section-content">
    <h3>Leadership in the Age of AI Agents</h3>
    <p>Exploring how leadership models adapt when executives oversee both human teams and autonomous AI systems. This includes applying the Nadler–Tushman Congruence Model to align strategy, structure, work, and culture in organizations where AI agents carry out core functions alongside human staff.</p>
    <h3>Workflow Patterns for Human–AI Teams</h3>
    <p>Designing workflows that combine AI’s speed with human judgment. I study where to place humans in the loop, how to hand off work between people and machines, and how to make collaboration predictable.</p>
    <h3>Trust, Transparency, and Control</h3>
    <p>AI systems must be explainable, predictable, and adjustable. I explore ways to make capabilities visible, boundaries clear, and decisions accountable—grounded in Zero Trust principles and clean, reliable data.</p>

    <h3>From Prototype to Production</h3>
    <p>Bridging the gap between experimental AI and dependable tools. I focus on moving from stochastic, exploratory systems to deterministic, rule-bound automation that can be trusted in production.</p>

    <h3>Augmenting Knowledge Work</h3>
    <p>Using AI to make professionals faster, sharper, and better informed. This includes applications in decision-making, research, and knowledge management—always with the goal of leaving people more capable than when they started.</p>

    <h3>Automation, Work, and Human Dignity</h3>
    <p>Exploring how automation can remove the dumb, dirty, dangerous, and tedious work while creating new, meaningful roles. I research approaches to skill elevation, job design, and economic adaptation so technology expands the value of human contribution instead of displacing it without purpose.</p>
  </div>
</section>

<section id="writing" class="section">
  <h2 class="section-title">Writing</h2>
  <div class="section-content">
    {% assign posts = site.posts | sort: 'date' | reverse %}
    {% if posts and posts.size > 0 %}
      <p>Notes, essays, and examples drawn from my research in workflow design, trust and transparency, prototype-to-production transitions, knowledge work augmentation, the future of work in an automated economy, and leadership in organizations where AI agents work alongside human teams.</p>
      <ul class="posts-list">
        {% for post in posts limit:10 %}
          <li class="post-item">
            <h3 class="post-item-title">
              <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
            </h3>
            <div class="post-item-date">{{ post.date | date: "%B %d, %Y" }}</div>
            <div class="post-item-excerpt">
              {{ post.excerpt | default: post.content | strip_html | truncate: 200 }}
            </div>
          </li>
        {% endfor %}
      </ul>
    {% else %}
      <p>More writing soon. I’ll share practical examples from my research on human–AI collaboration, transparent workflows, the future of work, and leadership in AI-driven organizations.</p>
    {% endif %}
  </div>
</section>

<section id="resume" class="section">
  <h2 class="section-title">Resume</h2>
  <div class="section-content">
    <p>mcconnell.chris@icloud.com | (202) 341–8344 | LinkedIn: <a href="https://www.linkedin.com/in/c-mcconnell">c-mcconnell</a> | GitHub: <a href="https://github.com/miqcie">@miqcie</a></p>
    
    <p><strong>Technical Account Executive | Sales + Implementation | PostHog Contributor</strong></p>

    <h3>EXPERIENCE</h3>

    <h4>PostHog | Contributor (2025-Present)</h4>
    <ul>
      <li>Contributed dynamic LinkedIn sharing feature via GitHub <a href="https://github.com/PostHog/posthog.com/pull/12507">PR #12507</a></li>
      <li>Completed PostHog Academy Post-it Note certification</li>
      <li>Implemented analytics on 2 personal sites</li>
      <li><strong>Pizza Toppings:</strong> Supreme (pineapple=Switzerland)</li>
    </ul>

    <h4>Deep Water Point & Associates | Director, Sales & Operations (2021-2025)</h4>
    <ul>
      <li><strong>$500K enterprise deal</strong> closed through consultative selling and technical discovery</li>
      <li><strong>$400K savings</strong> delivered with Python automation (cut 160 hrs → 12 hrs)</li>
      <li><strong>300+ users secured</strong> with Zero Trust (NIST 800-171 compliant)</li>
      <li><strong>100+ consultants trained</strong> on secure AI adoption and technical tool implementation</li>
      <li>Improved sales forecasting accuracy by cleaning pipeline data and optimizing CPQ workflows</li>
    </ul>

    <h4>Style.me (SaaS Fashion Startup) | MBA Sales Manager (2020)</h4>
    <ul>
      <li><strong>50% lower inbound lead cost</strong> using A/B testing + funnel optimization in LinkedIn Campaign Manager</li>
      <li>Supported product-led growth from MVP → PMF</li>
    </ul>

    <h4>Ermenegildo Zegna | Sales Director (2018-2019)</h4>
    <ul>
      <li><strong>$4M P&L managed</strong> with 7-person team</li>
      <li><strong>$500K revenue growth</strong> through CxO engagement + relationships</li>
    </ul>

    <h4>Saks Fifth Avenue | Sales Manager (2013-2018)</h4>
    <ul>
      <li><strong>Scaled sales $4.5M → $6M</strong> leading 15-person team</li>
      <li>Launched digital selling platforms driving omni-channel adoption</li>
      <li>Managed <strong>20+ vendor relationships</strong> and product training programs</li>
    </ul>

    <h3>SPEAKING & RECOGNITION</h3>
    <ul>
      <li>Featured by 1Password at NASDAQ & <a href="https://blog.1password.com/rsac-2025-recap-with-1password">RSA Conference 2025</a> for human-centric security implementation</li>
      <li>Guest lecturer: NYU Stern MBA & VCU Executive MBA programs on stakeholder management</li>
    </ul>

    <h3>TECHNICAL SKILLS</h3>
    <p><strong>Analytics:</strong> PostHog, Google Analytics, Power BI<br>
    <strong>Sales:</strong> Salesforce, Apollo, LinkedIn Navigator<br>
    <strong>Implementation:</strong> Python automation, API integrations, Zapier, Postman, SQL</p>

    <h3>EDUCATION</h3>
    <p><strong>MBA Strategy & Analytics</strong>, NYU Stern | <strong>BA English</strong>, University of Idaho</p>

    <p><a href="{{ '/assets/resume/Chris_McConnell_PostHog_TAE.pdf' | relative_url }}">📄 Download PDF Resume</a></p>
  </div>
</section>

<section id="contact" class="section">
  <h2 class="section-title">Contact</h2>
  <div class="section-content">
    <div class="contact-info">
      <p>I'm interested in conversations about applied AI, human–AI workflow design, Zero Trust security, the future of work, and leadership in AI-driven organizations.</p>
      <p>
        Email: <a href="mailto:chris@humaine.studio">chris@humaine.studio</a><br>
        Medium: <a href="https://medium.com/@humaine_studio" rel="me noopener">humaine_studio</a><br>
        LinkedIn: <a href="https://www.linkedin.com/in/c-mcconnell/" rel="me noopener">chrismcconnell</a>
      </p>
    </div>
  </div>
</section>