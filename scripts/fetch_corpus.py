"""One-time fetch: download the GitLab Handbook Security Policies & Standards
pages and assemble docs/source.md.

[MANUAL] Verify every URL below still resolves before trusting this run —
GitLab reorganizes handbook paths periodically. Failed pages are skipped and
reported at the end; fix the slug and re-run.

Usage: python scripts/fetch_corpus.py
"""
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md_convert

RAW_DIR = Path("docs/raw")
SOURCE_PATH = Path("docs/source.md")

PAGES = [
    ("Data Classification Standard", "https://handbook.gitlab.com/handbook/security/policies_and_standards/data-classification-standard/"),
    ("Password Standard", "https://handbook.gitlab.com/handbook/security/policies_and_standards/password-standard/"),
    ("Cryptographic Standard", "https://handbook.gitlab.com/handbook/security/policies_and_standards/cryptographic-standard/"),
    ("GitLab Internal Acceptable Use Policy", "https://handbook.gitlab.com/handbook/people-group/acceptable-use-policy/"),
    ("Backups of GitLab.com", "https://handbook.gitlab.com/handbook/engineering/gitlab-com/policies/backup/"),
    ("Monitoring of GitLab.com", "https://handbook.gitlab.com/handbook/engineering/gitlab-com/policies/monitoring/"),
    ("Penetration Testing Policy", "https://handbook.gitlab.com/handbook/security/security-and-technology-policies/penetration-testing-policy/"),
    ("Token Management Standard", "https://handbook.gitlab.com/handbook/security/policies_and_standards/token-management-standard/"),
    ("Physical Security Standard for Company Assets", "https://handbook.gitlab.com/handbook/security/policies_and_standards/physical-security-standard-for-company-assets/"),
    ("Records Retention & Disposal", "https://handbook.gitlab.com/handbook/security/policies_and_standards/records-retention-deletion/"),
    ("Security Logging Standards", "https://handbook.gitlab.com/handbook/security/policies_and_standards/security-logging-standard/"),
    ("Change Management Policy", "https://handbook.gitlab.com/handbook/security/security-and-technology-policies/change-management-policy/"),
    ("Audit Logging Policy", "https://handbook.gitlab.com/handbook/security/security-and-technology-policies/audit-logging-policy/"),
    ("Access Management Policy", "https://handbook.gitlab.com/handbook/security/security-and-technology-policies/access-management-policy/"),
    ("GitLab Security Compliance Controls", "https://handbook.gitlab.com/handbook/security/security-assurance/security-compliance/sec-controls/"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (DocuSense-ingest/1.0)"}


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def extract_main_content(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.select_one("main.td-content") or soup.select_one("article") or soup.select_one("main") or soup.body
    if main is None:
        return md_convert(html)
    for tag in main.select("nav, .td-toc, .td-breadcrumbs, script, style"):
        tag.decompose()
    return md_convert(str(main), heading_style="ATX")


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    combined = []

    for title, url in PAGES:
        print(f"Fetching: {title} <- {url}")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  !! FAILED ({e}) — verify/replace this URL manually.")
            continue

        markdown = extract_main_content(resp.text).strip()
        (RAW_DIR / f"{slugify(title)}.md").write_text(markdown, encoding="utf-8")
        combined.append(f"<!-- PAGE_BREAK -->\n## {title}\n\n<!-- source: {url} -->\n\n{markdown}\n")
        time.sleep(0.5)

    SOURCE_PATH.write_text("\n\n".join(combined), encoding="utf-8")
    print(f"\nWrote {len(combined)}/{len(PAGES)} pages to {SOURCE_PATH}")
    if len(combined) < len(PAGES):
        print("Some pages failed — fix the URLs above before running app.ingest.")


if __name__ == "__main__":
    main()