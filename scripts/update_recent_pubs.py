#!/usr/bin/env python
"""
Fetch recent publications by Garavito-Camargo from the NASA ADS API
and update the "Recent Papers" section in _pages/cv_pub.md.

Usage:
    # Update with papers from the last 12 months (default):
    python scripts/update_recent_pubs.py

    # Update with papers from the last 18 months:
    python scripts/update_recent_pubs.py --months 18

    # Preview without writing (dry-run):
    python scripts/update_recent_pubs.py --dry-run

    # Use a custom ADS token (overrides env variable):
    python scripts/update_recent_pubs.py --token YOUR_TOKEN

Environment:
    ADS_TOKEN  –  Your NASA ADS API token.
                  Get one at https://ui.adsabs.harvard.edu/user/settings/token

Output:
    Overwrites the "### Recent Papers" section in _pages/cv_pub.md
    while leaving the rest of the file (including "### Highlighted Papers")
    untouched.
"""

import argparse
import os
import re
import sys
import tempfile
from datetime import datetime, timedelta

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ── ADS API configuration ────────────────────────────────────────────────────
ADS_SEARCH_URL = "https://api.adsabs.harvard.edu/v1/search/query"
FIELDS = "title,author,pubdate,pub,bibcode,doctype,year"
QUERY = 'author:"garavito-camargo" collection:astronomy'
ROWS = 200
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
RETRY_STATUS_CODES = (429, 500, 502, 503, 504)

# ── File paths (relative to repo root) ───────────────────────────────────────
REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
CV_PUB_PATH = os.path.join(REPO_ROOT, "_pages", "cv_pub.md")

# ── Section markers ──────────────────────────────────────────────────────────
RECENT_HEADER = "### Recent Papers"


# ─────────────────────────────────────────────────────────────────────────────
# ADS helpers
# ─────────────────────────────────────────────────────────────────────────────

def build_session():
    """Return a requests session configured with retry/backoff behavior."""
    retry = Retry(
        total=MAX_RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=RETRY_STATUS_CODES,
        allowed_methods=("GET",),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def parse_ads_response(data):
    """Validate ADS response shape and return (num_found, docs)."""
    response = data.get("response")
    if not isinstance(response, dict):
        raise RuntimeError("ADS response missing 'response' object")

    num_found = response.get("numFound")
    docs = response.get("docs")

    if not isinstance(num_found, int):
        raise RuntimeError("ADS response has invalid 'numFound'")
    if not isinstance(docs, list):
        raise RuntimeError("ADS response has invalid 'docs' list")

    return num_found, docs


def fetch_papers(token, cutoff_date, timeout=DEFAULT_TIMEOUT):
    """
    Fetch papers from ADS published on or after *cutoff_date*.
    Returns a list of paper dicts sorted by date descending.
    """
    headers = {"Authorization": f"Bearer {token}"}

    # ADS pubdate filter: YYYY-MM
    cutoff_str = cutoff_date.strftime("%Y-%m")
    fq = f"pubdate:[{cutoff_str} TO *]"

    params = {
        "q": QUERY,
        "fl": FIELDS,
        "rows": ROWS,
        "sort": "date desc",
        "fq": fq,
    }

    docs = []
    num_found = None
    session = build_session()

    while num_found is None or len(docs) < num_found:
        if docs:
            params["start"] = len(docs)
        resp = session.get(
            ADS_SEARCH_URL,
            params=params,
            headers=headers,
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        num_found, response_docs = parse_ads_response(data)
        docs.extend(response_docs)
        if not response_docs:
            break

    # Sort by pubdate descending
    docs.sort(key=lambda p: p.get("pubdate", "0000"), reverse=True)
    return docs


def is_proceeding(paper):
    """True for conference abstracts, proceedings, proposals, etc."""
    skip_types = {
        "abstract", "inproceedings", "proposal", "erratum",
        "phdthesis", "dataset", "catalog",
    }
    return paper.get("doctype", "") in skip_types


def is_white_paper(paper):
    """True for BAAS white papers and known white-paper eprints."""
    pub = paper.get("pub", "").lower()
    title = paper.get("title", [""])[0].lower()
    if "bulletin of the american astronomical" in pub:
        return True
    if paper.get("doctype") == "eprint":
        wp_keywords = ["nancy", "rubin observatory", "from data to software"]
        if any(kw in title for kw in wp_keywords):
            return True
    return False


def filter_papers(papers):
    """Keep only refereed articles and submitted eprints (no proceedings, white papers)."""
    return [
        p for p in papers
        if not is_proceeding(p) and not is_white_paper(p)
    ]


# ─────────────────────────────────────────────────────────────────────────────
# Markdown formatting
# ─────────────────────────────────────────────────────────────────────────────

def abbreviate_name(full_name):
    """
    Convert 'Last, First Middle' → 'Last, F. M.'
    Handles hyphenated first names and suffixes.
    """
    parts = full_name.split(", ", 1)
    if len(parts) < 2:
        return full_name
    last = parts[0]
    firsts = parts[1].split()
    initials = []
    for f in firsts:
        # Handle hyphenated first names like "Chervin F. P."
        if "-" in f:
            sub = f.split("-")
            initials.append("-".join(s[0] + "." for s in sub if s))
        elif len(f) == 1 or (len(f) == 2 and f.endswith(".")):
            initials.append(f if f.endswith(".") else f + ".")
        else:
            initials.append(f[0] + ".")
    return f"{last}, {' '.join(initials)}"


def format_authors(authors, max_authors=10):
    """
    Format author list for Markdown.
    Bold 'Garavito-Camargo'. Truncate after *max_authors*.
    """
    formatted = []
    for a in authors[:max_authors]:
        name = abbreviate_name(a)
        if "garavito" in a.lower():
            name = f"**{name}**"
        formatted.append(name)
    author_str = "; ".join(formatted)
    if len(authors) > max_authors:
        author_str += "; et al."
    return author_str


def format_date(pubdate):
    """Convert ADS pubdate '2024-11-00' → 'November 2024'."""
    try:
        parts = pubdate.split("-")
        year = parts[0]
        month = int(parts[1]) if len(parts) > 1 else 0
        if month > 0:
            month_name = datetime(2000, month, 1).strftime("%B")
            return f"{month_name} {year}"
        return year
    except Exception:
        return pubdate


def format_journal(paper):
    """Return a short journal string, e.g. 'ApJ', 'MNRAS', 'arXiv'."""
    pub = paper.get("pub", "")
    doctype = paper.get("doctype", "")

    # Map common full journal names to abbreviations
    journal_map = {
        "The Astrophysical Journal": "ApJ",
        "The Astronomical Journal": "AJ",
        "Monthly Notices of the Royal Astronomical Society": "MNRAS",
        "Astronomy and Astrophysics": "A&A",
        "Astronomy & Astrophysics": "A&A",
        "Nature": "Nature",
        "Nature Astronomy": "Nature Astronomy",
        "The Astrophysical Journal Supplement Series": "ApJS",
        "The Astrophysical Journal Letters": "ApJL",
        "Journal of Cosmology and Astroparticle Physics": "JCAP",
        "The Journal of Open Source Software": "JOSS",
        "Physical Review D": "PRD",
        "Physical Review Letters": "PRL",
    }

    for full_name, abbrev in journal_map.items():
        if full_name.lower() in pub.lower():
            return abbrev

    if doctype == "eprint":
        return "arXiv"

    # Fallback: return the raw pub string (often already abbreviated)
    return pub if pub else "arXiv"


def format_paper_md(paper):
    """Format a single paper as a Markdown list item matching the cv_pub.md style."""
    title = paper.get("title", ["Untitled"])[0]
    authors = paper.get("author", ["Unknown"])
    pubdate = paper.get("pubdate", "")
    bibcode = paper.get("bibcode", "")

    ads_url = f"https://ui.adsabs.harvard.edu/abs/{bibcode}/abstract"
    date_str = format_date(pubdate)
    journal = format_journal(paper)
    author_str = format_authors(authors)

    line = f"- [{title}]({ads_url}).\n"
    line += f"  {author_str} *{journal}, {date_str}.*\n"
    return line


# ─────────────────────────────────────────────────────────────────────────────
# File update logic
# ─────────────────────────────────────────────────────────────────────────────

def read_cv_pub(path):
    """Read cv_pub.md and return its contents."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text_atomic(path, content):
    """Write text atomically to avoid partial updates on failure."""
    directory = os.path.dirname(os.path.abspath(path))
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=directory,
            delete=False,
        ) as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name
        os.replace(tmp_path, path)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


def replace_recent_section(content, new_entries):
    """
    Replace everything from '### Recent Papers' to the end of the file
    (or the next '###'/`---` section) with *new_entries*.
    """
    # Find the "### Recent Papers" header
    pattern = re.compile(
        r"(### Recent Papers\s*\n)(.*)",
        re.DOTALL,
    )
    match = pattern.search(content)
    if not match:
        # Section doesn't exist yet — append it at the end
        new_section = f"\n{RECENT_HEADER}\n\n{new_entries}\n"
        return content.rstrip() + "\n\n---\n" + new_section

    # Keep everything before the recent papers content
    before = content[: match.start(2)]
    new_content = before + "\n" + new_entries + "\n"
    return new_content


def build_recent_section(papers):
    """Build the Markdown content for the Recent Papers section."""
    lines = []
    for paper in papers:
        lines.append(format_paper_md(paper))
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Update the Recent Papers section in cv_pub.md from NASA ADS.",
    )
    parser.add_argument(
        "--months",
        type=int,
        default=12,
        help="Include papers from the last N months (default: 12).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the updated section without writing to the file.",
    )
    parser.add_argument(
        "--token",
        type=str,
        default=None,
        help="ADS API token. Overrides the ADS_TOKEN environment variable.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path. Defaults to _pages/cv_pub.md in the repo.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="HTTP timeout in seconds for ADS API calls (default: 30).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Resolve ADS token
    token = args.token or os.environ.get("ADS_TOKEN")
    if not token:
        print(
            "Error: No ADS API token provided.\n"
            "Set the ADS_TOKEN environment variable or use --token.\n"
            "Get a token at https://ui.adsabs.harvard.edu/user/settings/token",
            file=sys.stderr,
        )
        sys.exit(1)

    # Compute cutoff date
    cutoff = datetime.now() - timedelta(days=args.months * 30)
    print(f"Fetching papers from ADS (since {cutoff.strftime('%Y-%m')}) …")

    if args.timeout <= 0:
        print("Error: --timeout must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    try:
        papers = fetch_papers(token, cutoff, timeout=args.timeout)
    except (requests.RequestException, RuntimeError, ValueError) as exc:
        print(f"Error: Failed to fetch papers from ADS: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"  Found {len(papers)} total results from ADS.")

    papers = filter_papers(papers)
    print(f"  After filtering (no proceedings/white papers): {len(papers)} papers.")

    if not papers:
        print("  No recent papers found. Nothing to update.")
        return

    # Build the new section content
    section_md = build_recent_section(papers)

    if args.dry_run:
        print(f"\n{'─' * 60}")
        print(f"{RECENT_HEADER}\n")
        print(section_md)
        print(f"{'─' * 60}")
        print("\nDry run — no files were modified.")
        return

    # Read existing file and replace section
    cv_pub_path = args.output or CV_PUB_PATH
    if not os.path.exists(cv_pub_path):
        print(f"Error: File not found: {cv_pub_path}", file=sys.stderr)
        sys.exit(1)

    content = read_cv_pub(cv_pub_path)
    updated = replace_recent_section(content, section_md)

    write_text_atomic(cv_pub_path, updated)

    print(f"  Updated {cv_pub_path} with {len(papers)} recent papers.")
    print("  Done! Review the changes and commit when ready.")


if __name__ == "__main__":
    main()
