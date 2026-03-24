---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

<div class="about-hero">
  <p class="about-hero__lead">I use data science and AI to understand how cities work — and to help make them fairer, greener, and better served. My research spans <strong>urban analytics</strong>, <strong>human mobility</strong>, and <strong>computational social science</strong>, with a deliberate focus on turning research into real-world policy impact.</p>
  <p class="about-hero__lead" style="margin-top:0.6em; font-size:0.95em !important;">Published in <em>Nature Human Behaviour</em> · covered by the BBC, <em>Science</em> and <em>Wired</em> in 15+ countries · evidence to UK Parliament and government departments.</p>
  <div class="about-hero__tags">
    <span class="hero-tag">Urban Analytics</span>
    <span class="hero-tag">Human Mobility</span>
    <span class="hero-tag">Data Science for Policy</span>
    <span class="hero-tag">AI &amp; Society</span>
  </div>
</div>

## What I Work On

<div class="research-themes">
  <div class="theme-card">
    <h3>🏙️ Urban Analytics</h3>
    <p>Understanding how cities function through mobile phone data, social media, and other digital traces — from crowd size estimation to urban vibrancy to access to greenspace.</p>
  </div>
  <div class="theme-card">
    <h3>🚌 Transport &amp; Mobility</h3>
    <p>Analysing patterns of human movement to understand inequality in access to transport, the affordability of public transit, and how COVID-19 restructured people's mobility.</p>
  </div>
  <div class="theme-card">
    <h3>📊 Data Science for Policy</h3>
    <p>Bridging cutting-edge research and government decision-making — providing evidence to Parliament and co-designing research with teams at the Department for Transport, ONS, and 10 Downing Street.</p>
  </div>
  <div class="theme-card">
    <h3>🤖 AI &amp; Society</h3>
    <p>Exploring how AI and large-scale data can be used responsibly and equitably, while addressing questions of bias, access, and public trust in data-driven systems.</p>
  </div>
</div>

---

## Impact in Numbers

<div class="stats-grid">
  <div class="stat-item">
    <span class="stat-number" data-target="19">0</span>
    <span class="stat-label">peer-reviewed publications</span>
  </div>
  <div class="stat-item">
    <span class="stat-number" data-target="1.6" data-decimal="true">0</span>
    <span class="stat-label">£M+ in research grants</span>
  </div>
  <div class="stat-item">
    <span class="stat-number" data-target="4">0</span>
    <span class="stat-label">Parliamentary Select Committees</span>
  </div>
  <div class="stat-item">
    <span class="stat-number" data-target="8">0</span>
    <span class="stat-label">PhD students supervised</span>
  </div>
  <div class="stat-item">
    <span class="stat-number" data-target="15">0</span>
    <span class="stat-label">countries with media coverage</span>
  </div>
  <div class="stat-item">
    <span class="stat-number" data-target="3">0</span>
    <span class="stat-label">postdoctoral researchers</span>
  </div>
</div>

---

## Recent Highlights

- **2025** — Appointed Programme Lead for Exeter's new **MSc in AI for the Environment**
- **2025** — New research on healthcare access inequalities (*Journal of Physics: Complexity*) and rail journey costs (*Environment and Planning B*)
- **2024** — General Chair of the **Conference on Complex Systems (CCS2024)**, the world's flagship conference in complex systems science
- **2024** — Gave **oral evidence to the Transport Select Committee** on the future of transport data
- **2024** — Appointed **Deputy Director of Education (PGT)** at Exeter
- **2023** — Published in *Nature Human Behaviour* on how COVID-19 restructured human mobility across space and time
- **2021–2023** — **ESRC No. 10 Data Science Fellow**, embedded with the data science team at **10 Downing Street** and the ONS Data Science Campus

---

## Working with Partners

<div class="partners-section">
I actively seek collaborations with organisations outside academia — particularly in government, the public sector, and mission-driven industry. If you are working on challenges involving transport, cities, data, or AI and want to explore a research partnership, I welcome a conversation.

<strong>Previous partners include:</strong> Department for Transport · Office for National Statistics · 10 Downing Street Data Science Team · Natural England · DEFRA · Foreign, Commonwealth and Development Office · LV= / Allianz Insurance · City Science
</div>

[Get in touch](mailto:f.botta@exeter.ac.uk){: .btn .btn--primary}
&nbsp;&nbsp;[View my research](/publications/){: .btn}
&nbsp;&nbsp;[Policy &amp; impact](/policy/){: .btn}

---

## Current Projects

I am currently involved in a number of funded research projects in collaboration with government and industry partners, focusing on transport equity, urban environments, AI applications, and access to natural spaces. I also have an ongoing knowledge exchange project with the **Royal Albert Memorial Museum (RAMM)** in Exeter, using data science to better understand and predict visitor patterns.

<script>
document.addEventListener('DOMContentLoaded', function() {
  var counters = document.querySelectorAll('.stat-number[data-target]');

  function animateCounter(el) {
    var target = parseFloat(el.getAttribute('data-target'));
    var isDecimal = el.getAttribute('data-decimal') === 'true';
    var duration = 1800;
    var start = performance.now();

    function update(now) {
      var elapsed = now - start;
      var progress = Math.min(elapsed / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var value = eased * target;
      el.textContent = isDecimal ? value.toFixed(1) : Math.floor(value);
      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        el.textContent = isDecimal ? target.toFixed(1) : target;
      }
    }
    requestAnimationFrame(update);
  }

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
    counters.forEach(function(el) { observer.observe(el); });
  } else {
    counters.forEach(function(el) { animateCounter(el); });
  }
});
</script>
