---
layout: archive
title: "Peer Review"
permalink: /reviewing/
author_profile: true
---

I have been an active peer reviewer since 2013, contributing to {{ site.data.peer_review.journals | size }} journals across urban analytics, data science, complex systems, transport, and related fields. New journals are discovered automatically via my [ORCID profile](https://orcid.org/0000-0002-5681-4535){:target="_blank"}.

---

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
