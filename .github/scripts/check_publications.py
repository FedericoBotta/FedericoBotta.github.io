#!/usr/bin/env python3
"""
check_publications.py
─────────────────────
Queries OpenAlex for publications by ORCID 0000-0002-5681-4535,
compares them with the current _pages/publications.md, and inserts
any new papers in the correct year position.

If new papers are found it writes:
  • new_papers_found=true  → GITHUB_OUTPUT  (triggers the PR step)
  • PR_TITLE / PR_BODY     → GITHUB_ENV     (used by create-pull-request)
"""

import os
import re
import sys
import json
import requests
from difflib import SequenceMatcher
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

ORCID = "0000-0002-5681-4535"
CONTACT_EMAIL = "f.botta@exeter.ac.uk"   # included in User-Agent per OA policy

OPENALEX_URL = (
    "https://api.openalex.org/works"
    f"?filter=author.orcid:{ORCID}"
    "&per-page=50"
    "&sort=publication_year:desc"
    "&select=id,title,publication_year,type,doi,cited_by_count"
    ",authorships,primary_location,biblio"
)

REPO_ROOT       = Path(__file__).resolve().parents[2]
PUBLICATIONS_MD = REPO_ROOT / "_pages" / "publications.md"
EXCLUDED_FILE   = Path(__file__).parent / "excluded_dois.txt"

# ── Noise filters ─────────────────────────────────────────────────────────────

# Work types to always skip
SKIP_TYPES = {
    "peer-review", "dissertation", "paratext",
    "erratum", "editorial", "retraction",
}

# If the source name contains any of these substrings → skip
# (Zenodo = data deposits; SSRN = duplicate archive; Qeios = review platform)
SKIP_SOURCE_SUBSTRINGS = ["zenodo", "qeios", "ssrn", "dissem.in"]

# Title prefixes / patterns that indicate noise records
SKIP_TITLE_PATTERNS = [
    r"^author response",
    r"^review of[:\s]",
    r"^review for[:\s]",
    r"agrifood campaign",
    r"urban analytics series",   # seminar recording abstract
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def normalise(text: str) -> str:
    """Lowercase + strip punctuation for fuzzy comparison."""
    return re.sub(r"[^\w\s]", "", text.lower()).strip()


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalise(a), normalise(b)).ratio()


def doi_clean(work: dict) -> str:
    raw = (work.get("doi") or "").replace("https://doi.org/", "").strip()
    return raw.lower()


def source_display(work: dict) -> str:
    return (
        (work.get("primary_location") or {})
        .get("source") or {}
    ).get("display_name", "").lower()


def is_preprint(work: dict) -> bool:
    if work.get("type") == "preprint":
        return True
    src = source_display(work)
    return any(s in src for s in ["arxiv", "biorxiv", "medrxiv", "posted content"])


def format_authors(authorships: list) -> str:
    """Convert OpenAlex authorships → 'Surname, F., &amp; Surname2, F2.'"""
    names = []
    for entry in authorships:
        display = (entry.get("author") or {}).get("display_name", "")
        parts = display.split()
        if not parts:
            continue
        surname = parts[-1]
        initials = "".join(p[0] + "." for p in parts[:-1] if p)
        names.append(f"{surname}, {initials}" if initials else surname)

    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + ", &amp; " + names[-1]


def format_venue(work: dict) -> str:
    """Build venue string with volume/issue/pages when available."""
    src_name = (
        (work.get("primary_location") or {})
        .get("source") or {}
    ).get("display_name", "")

    b = work.get("biblio") or {}
    vol, issue = b.get("volume"), b.get("issue")
    fp, lp = b.get("first_page"), b.get("last_page")

    venue = src_name
    if vol:
        venue += f", {vol}"
        if issue:
            venue += f"({issue})"
    if fp:
        venue += f", {fp}"
        if lp and lp != fp:
            venue += f"–{lp}"
    return venue


def html_entry(work: dict) -> str:
    """Render one publication-item div matching the site's existing markup."""
    year    = work.get("publication_year", "")
    title   = (work.get("title") or "").strip()
    authors = format_authors(work.get("authorships", []))
    venue   = format_venue(work)
    doi     = doi_clean(work)

    preprint_tag = ' <em>(preprint)</em>' if is_preprint(work) else ''
    doi_badge = (
        f'\n<a href="https://doi.org/{doi}" class="pub-badge" '
        f'target="_blank" rel="noopener">doi</a>'
    ) if doi else ''

    return (
        f'<div class="publication-item" data-year="{year}">\n'
        f'<span class="pub-year">{year}</span>\n'
        f'<span class="pub-title">{title}</span>{preprint_tag}<br>\n'
        f'{authors}<br>\n'
        f'<span class="pub-venue">{venue}</span>{doi_badge}\n'
        f'</div>'
    )

# ── GitHub Actions output helpers ─────────────────────────────────────────────

def gh_output(key: str, value: str):
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a") as f:
            f.write(f"{key}={value}\n")


def gh_env(key: str, value: str, multiline: bool = False):
    path = os.environ.get("GITHUB_ENV")
    if path:
        with open(path, "a") as f:
            if multiline:
                delim = f"EOF_{key}"
                f.write(f"{key}<<{delim}\n{value}\n{delim}\n")
            else:
                f.write(f"{key}={value}\n")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Load current publications page
    pub_text = PUBLICATIONS_MD.read_text(encoding="utf-8")

    # Extract titles already on the page
    existing_titles = [
        t.strip()
        for t in re.findall(
            r'<span class="pub-title">(.*?)</span>', pub_text, re.DOTALL
        )
    ]

    # Extract DOIs already on the page
    existing_dois = {
        d.lower().strip()
        for d in re.findall(r'doi\.org/([^\s"\'<\n]+)', pub_text)
    }

    # Load permanently excluded DOIs (added by user to skip unwanted papers)
    excluded_dois: set[str] = set()
    if EXCLUDED_FILE.exists():
        for line in EXCLUDED_FILE.read_text().splitlines():
            line = line.strip().lower()
            if line and not line.startswith("#"):
                excluded_dois.add(line)

    # Fetch works from OpenAlex
    headers = {
        "User-Agent": f"FedericoBotta-website-bot/1.0 (mailto:{CONTACT_EMAIL})"
    }
    resp = requests.get(OPENALEX_URL, headers=headers, timeout=30)
    resp.raise_for_status()
    works = resp.json().get("results", [])
    print(f"OpenAlex returned {len(works)} records.")

    new_papers = []

    for work in works:
        title  = (work.get("title") or "").strip()
        wtype  = work.get("type", "")
        doi    = doi_clean(work)
        src    = source_display(work)

        # ── Noise filters ──────────────────────────────────────────────────

        if wtype in SKIP_TYPES:
            continue

        if any(s in src for s in SKIP_SOURCE_SUBSTRINGS):
            continue

        if any(re.search(p, title, re.IGNORECASE) for p in SKIP_TITLE_PATTERNS):
            continue

        # ── Deduplication ──────────────────────────────────────────────────

        # Permanently excluded by user
        if doi and doi in excluded_dois:
            continue

        # DOI already on the page
        if doi and doi in existing_dois:
            continue

        # Title too similar to something already listed
        # (catches preprints whose published version is already listed)
        if any(similarity(title, t) > 0.80 for t in existing_titles):
            continue

        new_papers.append(work)

    if not new_papers:
        print("✓ No new papers found — nothing to do.")
        return

    print(f"Found {len(new_papers)} new paper(s):")
    for w in new_papers:
        print(f"  + {w.get('title', '?')} ({w.get('publication_year', '?')})")

    # ── Insert new papers into publications.md ─────────────────────────────

    year_re = re.compile(r'<div class="publication-item[^"]*" data-year="(\d+)">')

    for work in new_papers:
        year  = int(work.get("publication_year") or 0)
        entry = html_entry(work)

        # Find insertion point: just before the first paper with an older year
        matches = list(year_re.finditer(pub_text))
        insert_pos = None
        for m in matches:
            if int(m.group(1)) < year:
                insert_pos = m.start()
                break

        if insert_pos is None:
            # Newer than everything, or same year group — go before closing </div>
            close = pub_text.rfind('\n</div>\n\n<script')
            insert_pos = close if close != -1 else pub_text.rfind('</div>\n\n</div>')

        pub_text = pub_text[:insert_pos] + entry + "\n\n" + pub_text[insert_pos:]

    PUBLICATIONS_MD.write_text(pub_text, encoding="utf-8")
    print("✓ publications.md updated.")

    # ── Build PR title and body ────────────────────────────────────────────

    n = len(new_papers)
    plural = "s" if n > 1 else ""
    pr_title = f"📚 {n} new publication{plural} found via OpenAlex"

    body_lines = [
        f"## {n} new publication{plural} found via OpenAlex\n",
        "The workflow found the following paper(s) in OpenAlex that are not yet on your site.",
        "Please **review the diff**, adjust formatting if needed (year, venue, ★ highlight),",
        "then **Merge** to publish or **Close** to skip.\n",
        "> **To permanently skip a paper** (so it is never proposed again), add its DOI",
        "> to `.github/scripts/excluded_dois.txt` before closing this PR.\n",
        "---\n",
    ]

    for work in new_papers:
        title     = (work.get("title") or "").strip()
        year      = work.get("publication_year", "?")
        venue     = format_venue(work)
        doi       = doi_clean(work)
        citations = work.get("cited_by_count", 0)
        wtype     = "preprint" if is_preprint(work) else work.get("type", "")

        body_lines += [
            f"### {title}",
            f"- **Year:** {year}",
            f"- **Type:** {wtype}",
            f"- **Venue:** {venue or '(not yet available)'}",
            *([ f"- **DOI:** https://doi.org/{doi}" ] if doi else []),
            f"- **Citations (OpenAlex):** {citations}",
            "",
        ]

    body_lines += [
        "---",
        "_Opened automatically by the "
        "[OpenAlex publications workflow](/.github/workflows/update-publications.yml)._",
    ]

    pr_body = "\n".join(body_lines)

    # Write outputs for the GitHub Actions workflow
    gh_output("new_papers_found", "true")
    gh_env("PR_TITLE", pr_title)
    gh_env("PR_BODY", pr_body, multiline=True)


if __name__ == "__main__":
    main()
