---
layout: home
title: "Humaine Studio"
---

<div class="hero">
  <h1 class="hero-title">Chris McConnell</h1>
  <p class="hero-subtitle">Applied AI researcher exploring human-machine collaboration.</p>
  <p class="hero-description">
    I work on the intersection of artificial intelligence and human judgment, focusing on real-world applications that augment rather than replace human decision-making. My research centers on building trust in AI systems through transparent, collaborative workflows.
  </p>
</div>

<section id="philosophy" class="section">
  <h2 class="section-title">Philosophy</h2>
  <div class="section-content">
    <p>
      The most interesting problems in AI aren't purely technical—they're human. As we integrate AI into our workflows, the critical challenge is maintaining human agency while leveraging machine capabilities.
    </p>
    <p>
      I believe in the "missing middle"—the space where machines assist but humans still decide. This isn't about building systems that think for us, but systems that help us think better. The goal is augmentation, not automation.
    </p>
    <p>
      Trust in AI systems comes from understanding, not blind faith. The best human-AI collaborations are transparent, predictable, and leave humans in control of consequential decisions.
    </p>
  </div>
</section>

<section id="research" class="section">
  <h2 class="section-title">Research Areas</h2>
  <div class="section-content">
    <h3>Human-AI Workflow Design</h3>
    <p>
      How do we design workflows that leverage AI capabilities while preserving human expertise and judgment? I explore patterns for effective human-AI collaboration across different domains and decision contexts.
    </p>

    <h3>Trust and Transparency in AI Systems</h3>
    <p>
      Building AI systems that professionals can trust requires more than accuracy—it requires explainability, predictability, and clear boundaries. I research methods for creating transparent AI tools that professionals actually want to use.
    </p>

    <h3>Practical AI Implementation</h3>
    <p>
      The gap between AI research and real-world application is often enormous. I focus on bridging this gap through rapid prototyping, user feedback, and iterative design of AI-powered tools that solve actual problems.
    </p>

    <h3>Knowledge Work Augmentation</h3>
    <p>
      How can AI enhance rather than replace knowledge work? I explore applications in executive decision-making, research workflows, and professional knowledge management.
    </p>
  </div>
</section>

<section id="writing" class="section">
  <h2 class="section-title">Writing</h2>
  <div class="section-content">
    {% assign posts = site.posts | sort: 'date' | reverse %}
    {% if posts.size > 0 %}
      <ul class="posts-list">
        {% for post in posts limit:10 %}
          <li class="post-item">
            <h3 class="post-item-title">
              <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
            </h3>
            <div class="post-item-date">{{ post.date | date: "%B %d, %Y" }}</div>
            <div class="post-item-excerpt">
              {{ post.excerpt | strip_html | truncate: 200 }}
            </div>
          </li>
        {% endfor %}
      </ul>
    {% else %}
      <p>Writing coming soon. I share thoughts on AI research, human-machine collaboration, and practical applications of artificial intelligence in professional contexts.</p>
    {% endif %}
  </div>
</section>

<section id="contact" class="section">
  <h2 class="section-title">Contact</h2>
  <div class="section-content">
    <div class="contact-info">
      <p>I'm interested in conversations about applied AI research, human-AI collaboration patterns, and the practical challenges of implementing AI in professional workflows.</p>
      <p>
        Email: <a href="mailto:contact@humaine.studio">contact@humaine.studio</a><br>
        Twitter: <a href="https://twitter.com/humaine_studio">@humaine_studio</a><br>
        LinkedIn: <a href="https://linkedin.com/in/chrismcconnell">chrismcconnell</a>
      </p>
    </div>
  </div>
</section>