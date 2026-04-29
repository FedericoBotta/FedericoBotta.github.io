---
layout: archive
title: "Academic Service"
permalink: /service/
author_profile: true
---

<div class="service-intro">
I contribute to the academic community through editorial roles, conference organisation, society leadership, grant review, and peer reviewing for {{ site.data.peer_review.journals | size }} journals spanning urban analytics, data science, complex systems, transport, and related fields.
</div>

---

## Editorial Roles

<div class="service-section">
<table class="service-table">
  <tbody>
  {% assign current_editorial = site.data.service.editorial | where: "current", true | sort: "since" | reverse %}
  {% assign past_editorial = site.data.service.editorial | where: "current", false | sort: "since" | reverse %}
  {% for item in current_editorial %}
  <tr>
    <td class="service-period">{{ item.since }}–present</td>
    <td>
      <span class="service-role">{{ item.role }}</span>,
      <em>{{ item.journal }}</em>
      {% if item.note %}<br><span class="service-note">{{ item.note }}</span>{% endif %}
    </td>
  </tr>
  {% endfor %}
  {% for item in past_editorial %}
  <tr>
    <td class="service-period">{{ item.since }}</td>
    <td>
      <span class="service-role">{{ item.role }}</span>,
      <em>{{ item.journal }}</em>
      {% if item.note %}<br><span class="service-note">{{ item.note }}</span>{% endif %}
    </td>
  </tr>
  {% endfor %}
  </tbody>
</table>
</div>

---

## Conference Organisation

<div class="service-section">
<table class="service-table">
  <tbody>
  {% for item in site.data.service.conferences %}
  <tr>
    <td class="service-period">{% if item.period %}{{ item.period }}{% else %}{{ item.year }}{% endif %}</td>
    <td><span class="service-role">{{ item.role }}</span>, <em>{{ item.event }}</em></td>
  </tr>
  {% endfor %}
  </tbody>
</table>
</div>

---

## Society &amp; Committee Roles

<div class="service-section">
<table class="service-table">
  <tbody>
  {% for item in site.data.service.societies %}
  <tr>
    <td class="service-period">{{ item.period }}</td>
    <td><span class="service-role">{{ item.role }}</span>, <em>{{ item.organisation }}</em></td>
  </tr>
  {% endfor %}
  </tbody>
</table>
</div>

---

## Grant Review &amp; Funding Panels

<div class="service-section">
<ul class="service-list">
  {% for item in site.data.service.funding %}
  <li>
    <span class="service-role">{{ item.role }}</span> — {{ item.name }}{% if item.note %} <span class="service-note">({{ item.note }})</span>{% endif %}
  </li>
  {% endfor %}
</ul>
</div>

---

## Peer Review

<div class="service-intro" style="margin-bottom:1.2rem;">
Active reviewer since 2013 across {{ site.data.peer_review.journals | size }} journals. New journals are discovered automatically via my <a href="https://orcid.org/0000-0002-5681-4535" target="_blank">ORCID profile</a>.
</div>

<div id="reviewing-list">
{% assign groups = site.data.peer_review.journals | group_by: "since" | sort: "name" | reverse %}
{% for group in groups %}
<div class="review-group">
  <h3 class="review-since">Since {{ group.name }}</h3>
  <ul class="review-journal-list">
    {% assign sorted_journals = group.items | sort: "name" %}
    {% for journal in sorted_journals %}
    <li>{{ journal.name }}</li>
    {% endfor %}
  </ul>
</div>
{% endfor %}
</div>
