#!/usr/bin/env python3
"""
check_peer_reviews.py
─────────────────────
Fetches peer-review records from ORCID for 0000-0002-5681-4535,
resolves journal ISSNs to names via OpenAlex, and opens a PR if any
journal is found that is not yet in _data/peer_review.yml.

The manual list in peer_review.yml is the source of truth — this script
only ever ADDS new entries (journals newly credited via ORCID).
"""

import os
import re
import requests
import yaml
from difflib import SequenceMatcher
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

ORCID         = "0000-0002-5681-4535"
CONTACT_EMAIL = "f.botta@exeter.ac.uk"

ORCID_URL  = f"https://pub.orcid.org/v3.0/{ORCID}/peer-reviews"
OA_SOURCE  = "https://api.openalex.org/sources"

REPO_ROOT       = Path(__file__).resolve().parents[2]
PEER_REVIEW_YML = REPO_ROOT / "_data" / "peer_review.yml"

HEADERS = {"User-Agent": f"FedericoBotta-website-bot/1.0 (mailto:{CONTACT_EMAIL})"}

# ── Helpers ───────────────────────────────────────────────────────────────────

def normalise(text: str) -> str:
    return re.sub(r"[^\w\s]", "", text.lower()).strip()

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalise(a), normalise(b)).ratio()

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

# ── ORCID fetch ───────────────────────────────────────────────────────────────

def fetch_orcid_reviews() -> list[dict]:
    """
    Returns a list of dicts: {issn, first_year}
    one per unique ISSN group in the ORCID peer-review record.
    """
    resp = requests.get(
        ORCID_URL,
        headers={**HEADERS, "Accept": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    results = []
    for group in data.get("group", []):
        # Extract ISSN from the group's external-ids
        issn = None
        for eid in (group.get("external-ids") or {}).get("external-id", []):
            if eid.get("external-id-type") == "issn":
                issn = eid.get("external-id-value", "").strip()
                break
        if not issn:
            continue

        # Find earliest review year in this group
        years = []
        for summary in group.get("peer-review-summary", []):
            cd = summary.get("completion-date") or {}
            yr = (cd.get("year") or {}).get("value")
            if yr:
                try:
                    years.append(int(yr))
                except ValueError:
                    pass
        first_year = min(years) if years else None
        results.append({"issn": issn, "first_year": first_year})

    return results

# ── OpenAlex ISSN → journal name ──────────────────────────────────────────────

def resolve_issns(issns: list[str]) -> dict[str, str]:
    """Returns {issn: journal_display_name} for each resolvable ISSN."""
    if not issns:
        return {}

    # OpenAlex accepts up to ~50 ISSNs in one filter
    filter_str = "|".join(issns)
    resp = requests.get(
        OA_SOURCE,
        params={"filter": f"issn:{filter_str}", "per-page": 50},
        headers=HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    results = resp.json().get("results", [])

    mapping: dict[str, str] = {}
    for source in results:
        name = source.get("display_name", "").strip()
        for issn_val in source.get("issn", []) or []:
            mapping[issn_val] = name
        # Also index by the primary issn field if present
        primary = source.get("issn_l") or ""
        if primary:
            mapping[primary] = name

    return mapping

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Load existing journals from YAML
    raw = PEER_REVIEW_YML.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    existing = data.get("journals", [])
    existing_names = [j["name"] for j in existing]
    print(f"Loaded {len(existing_names)} journals from peer_review.yml")

    # Fetch ORCID records
    orcid_groups = fetch_orcid_reviews()
    print(f"ORCID returned {len(orcid_groups)} ISSN group(s).")

    # Resolve ISSNs to journal names
    issns = [g["issn"] for g in orcid_groups]
    issn_to_name = resolve_issns(issns)

    # Find journals in ORCID that are not yet in the YAML
    new_journals = []
    for group in orcid_groups:
        issn = group["issn"]
        name = issn_to_name.get(issn, "").strip()
        if not name:
            print(f"  Could not resolve ISSN {issn} — skipping.")
            continue

        # Check against existing list by title similarity
        if any(similarity(name, existing) > 0.85 for existing in existing_names):
            continue  # already in the list

        new_journals.append({
            "name":  name,
            "issn":  issn,
            "since": group["first_year"] or 2025,
        })
        print(f"  New journal found: {name} (ISSN {issn})")

    if not new_journals:
        print("✓ No new journals found — nothing to do.")
        return

    # Append new entries to the YAML (preserving existing content)
    year_group = {}
    for j in new_journals:
        year_group.setdefault(j["since"], []).append(j["name"])

    addition_lines = ["\n  # Added automatically via ORCID"]
    for year in sorted(year_group):
        for name in sorted(year_group[year]):
            addition_lines.append(f"  - name: {name}\n    since: {year}")

    # Insert before the final newline
    updated = raw.rstrip("\n") + "\n" + "\n".join(addition_lines) + "\n"
    PEER_REVIEW_YML.write_text(updated, encoding="utf-8")
    print(f"✓ peer_review.yml updated with {len(new_journals)} new journal(s).")

    # Build PR title and body
    n = len(new_journals)
    plural = "s" if n > 1 else ""
    pr_title = f"📋 {n} new peer-review journal{plural} found via ORCID"

    body_lines = [
        f"## {n} new journal{plural} found via ORCID\n",
        "The following journal(s) appeared in your ORCID peer-review record",
        "but are not yet in `_data/peer_review.yml`.\n",
        "Please check the **Since year** is correct (it reflects the earliest",
        "ORCID-credited review, which may not be when you first reviewed for",
        "that journal). Edit if needed, then **Merge** to publish or **Close** to skip.\n",
        "---\n",
    ]

    for j in new_journals:
        body_lines += [
            f"### {j['name']}",
            f"- **ISSN:** {j['issn']}",
            f"- **Since (from ORCID):** {j['since']}",
            f"- **OpenAlex:** https://api.openalex.org/sources?filter=issn:{j['issn']}",
            "",
        ]

    body_lines += [
        "---",
        "_Opened automatically by the "
        "[ORCID peer-review workflow](/.github/workflows/update-publications.yml)._",
    ]

    gh_output("new_journals_found", "true")
    gh_env("PR_TITLE_REVIEWS", pr_title)
    gh_env("PR_BODY_REVIEWS", "\n".join(body_lines), multiline=True)


if __name__ == "__main__":
    main()
