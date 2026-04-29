---
permalink: /
title: ""
excerpt: ""
layout: home
author_profile: false
redirect_from:
  - /about/
  - /about.html
hero_intro: "I use data science and AI to understand how cities work — and to help make them fairer, greener, and better served. My research spans urban analytics, human mobility, and computational social science, with a deliberate focus on turning research into real-world policy impact."
hero_tags:
  - Urban Analytics
  - Human Mobility
  - Data Science for Policy
  - AI & Society
---

## What I Work On

<div class="research-themes">
  <div class="theme-card">
    <h3>Urban Analytics</h3>
    <p>Understanding how cities function through mobile phone data, social media, and other digital traces — from crowd size estimation to urban vibrancy to access to greenspace.</p>
  </div>
  <div class="theme-card">
    <h3>Transport &amp; Mobility</h3>
    <p>Analysing patterns of human movement to understand inequality in access to transport, the affordability of public transit, and how COVID-19 restructured people's mobility.</p>
  </div>
  <div class="theme-card">
    <h3>Data Science for Policy</h3>
    <p>Bridging cutting-edge research and government decision-making — providing evidence to Parliament and co-designing research with teams at the Department for Transport, ONS, and 10 Downing Street.</p>
  </div>
  <div class="theme-card">
    <h3>AI &amp; Society</h3>
    <p>Exploring how AI and large-scale data can be used responsibly and equitably, while addressing questions of bias, access, and public trust in data-driven systems.</p>
  </div>
</div>

---

## Impact in Numbers

<div class="stats-grid">
  <div class="stat-item">
    <span class="stat-number" data-target="19">19</span>
    <span class="stat-label">peer-reviewed publications</span>
  </div>
  <div class="stat-item">
    <span class="stat-number" data-target="0.8" data-decimal="true">0.8</span>
    <span class="stat-label">£M+ in research grants</span>
  </div>
  <div class="stat-item">
    <span class="stat-number" data-target="4">4</span>
    <span class="stat-label">Parliamentary Select Committees</span>
  </div>
  <div class="stat-item">
    <span class="stat-number" data-target="8">8</span>
    <span class="stat-label">PhD students</span>
  </div>
  <div class="stat-item">
    <span class="stat-number" data-target="15">15</span>
    <span class="stat-label">countries with media coverage</span>
  </div>
  <div class="stat-item">
    <span class="stat-number" data-target="3">3</span>
    <span class="stat-label">postdoctoral researchers</span>
  </div>
  <a href="/reviewing/" class="stat-item">
    <span class="stat-number" data-target="{{ site.data.peer_review.journals | size }}">{{ site.data.peer_review.journals | size }}</span>
    <span class="stat-label">journals reviewed for</span>
  </a>
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

## Publication Highlights

<div class="paper-highlights">
  <div class="paper-card">
    <div class="paper-card__meta">2025 · Journal of Physics: Complexity</div>
    <h3 class="paper-card__title">Bus travel time variability and inequalities in healthcare access</h3>
    <p class="paper-card__summary">We show that where you live shapes how reliably you can reach hospital by bus — and that deprived communities in England face consistently higher travel time uncertainty, compounding existing access inequalities.</p>
    <a href="/papers/chen-2025.html" class="paper-card__link">Explore the research →</a>
  </div>
  <div class="paper-card">
    <div class="paper-card__meta">2024 · Environment and Planning B</div>
    <h3 class="paper-card__title">Spatiotemporal gender differences in urban vibrancy</h3>
    <p class="paper-card__summary">Using millions of app-usage records, we reveal that men and women experience the city differently in time and space — with women less present in public spaces at night and more concentrated in residential areas, reflecting broader patterns of urban inequality.</p>
    <a href="/papers/collins-2024.html" class="paper-card__link">Explore the research →</a>
  </div>
</div>

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

- **Bus transport accessibility across England** — Using national bus timetable data (BODS) to map how travel time variability affects access to healthcare and other essential services, with direct relevance to transport equity policy.
- **Greenspace and recreational value** — Quantifying the recreational and wellbeing value of landscape features across England.
- **Urban vibrancy and social sensing** — Ongoing work using mobile phone data, app usage data, and online traces to understand how different social groups experience and navigate urban environments.
- **Knowledge exchange with RAMM, Exeter** — Applying data science to visitor behaviour at the Royal Albert Memorial Museum to better understand and anticipate audience patterns.
- **Transport equity and journey costs** — Analysing the affordability and cost of public transport journeys.

---

## Prospective PhD Students

I welcome enquiries from prospective PhD students interested in working at the intersection of **data science, urban analytics, and social inequality**. Current areas of particular interest include public transport accessibility and equity, urban vibrancy and social sensing, human mobility modelling, and AI applications in environmental and social contexts.

Funding opportunities include EPSRC and ESRC Doctoral Training Partnerships (through the University of Exeter), as well as project-specific studentships — see the [University's postgraduate research pages](https://www.exeter.ac.uk/study/postgraduate/research/) for current opportunities. If you have a strong quantitative background and are motivated by research with real-world policy impact, feel free to [get in touch](mailto:f.botta@exeter.ac.uk) with a brief description of your interests.

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
