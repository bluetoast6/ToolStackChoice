#!/usr/bin/env python3
"""
apply_affiliates.py — ToolStackChoice affiliate link rewriter
=============================================================
Reads affiliates.json from the site root, then walks all HTML files
and rewrites outbound <a> tags pointing to affiliate-tracked domains
so they use:
  - The affiliate_url (if set) or the plain_url (if affiliate_url is null)
  - rel="sponsored noopener" on affiliate links
  - rel="nofollow noopener" on plain/fallback links
  - target="_blank" (unchanged from existing convention)

Usage (run from the site root):
  python3 scripts/apply_affiliates.py

To update a link later:
  1. Open affiliates.json
  2. Set "affiliate_url" for the relevant tool to the new URL
  3. Re-run this script

The script is idempotent — running it multiple times produces the same result.
"""

import json
import os
import re
import sys
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

SITE_ROOT = Path(__file__).parent.parent
CONFIG_FILE = SITE_ROOT / "affiliates.json"

# Files to skip (templates, internal pages, scripts themselves)
SKIP_FILES = {
    "tool-review-template.html",
    "tool-comparison-template.html",
    "faq-component.html",
    "compare-template.html",
    "comparison-table.html",
    "privacy.html",
    "about.html",
    "contact.html",
}

# Directories to skip entirely
SKIP_DIRS = {"scripts", ".git", "node_modules"}

# ── Domain → tool slug mapping ────────────────────────────────────────────────
# Maps URL hostname patterns to tool slugs in affiliates.json.
# Order matters: more specific patterns first.

DOMAIN_MAP = {
    "mangools.com": "mangools",
    "make.com": "make",
    "n8n.io": "n8n",
    "pabbly.com": "pabbly-connect",
    "moz.com": "moz-pro",
    "hostinger.com": "hostinger",
    "siteground.com": "siteground",
    "kinsta.com": "kinsta",
    "cloudways.com": "cloudways",
    "wordpress.com": "wordpress-com",
    "pressable.com": "pressable",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def effective_url(tool_cfg):
    """Return the affiliate URL if set, otherwise the plain URL."""
    return tool_cfg["affiliate_url"] or tool_cfg["plain_url"]


def is_affiliate(tool_cfg):
    return bool(tool_cfg.get("affiliate_url"))


def slug_for_url(url):
    """Return the tool slug for a given URL, or None if not tracked."""
    for domain, slug in DOMAIN_MAP.items():
        if domain in url:
            return slug
    return None


def rewrite_href(match, tools):
    """
    Regex replacement function.
    Receives a match object for an <a ...> tag and rewrites href/rel/target.
    """
    full_tag = match.group(0)
    href_match = re.search(r'href="([^"]+)"', full_tag)
    if not href_match:
        return full_tag

    original_href = href_match.group(1)
    slug = slug_for_url(original_href)
    if slug is None or slug not in tools:
        return full_tag

    tool_cfg = tools[slug]
    new_href = effective_url(tool_cfg)
    affiliate = is_affiliate(tool_cfg)
    new_rel = "sponsored noopener" if affiliate else "nofollow noopener"

    # Replace href value
    new_tag = re.sub(r'href="[^"]+"', f'href="{new_href}"', full_tag)

    # Replace or add rel attribute
    if re.search(r'\brel="[^"]*"', new_tag):
        new_tag = re.sub(r'rel="[^"]*"', f'rel="{new_rel}"', new_tag)
    else:
        new_tag = new_tag.replace("<a ", f'<a rel="{new_rel}" ', 1)

    # Ensure target="_blank" is present
    if 'target="_blank"' not in new_tag:
        new_tag = new_tag.replace("<a ", '<a target="_blank" ', 1)

    return new_tag


def process_file(filepath, tools):
    """Rewrite affiliate links in a single HTML file. Returns (changed, count)."""
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    # Match any <a ...> tag that contains an href pointing to a tracked domain
    pattern = re.compile(
        r'<a\b[^>]*href="https?://[^"]*(?:'
        + "|".join(re.escape(d) for d in DOMAIN_MAP.keys())
        + r')[^"]*"[^>]*>',
        re.IGNORECASE,
    )

    count = [0]

    def counted_rewrite(m):
        result = rewrite_href(m, tools)
        if result != m.group(0):
            count[0] += 1
        return result

    rewritten = pattern.sub(counted_rewrite, original)

    if rewritten != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(rewritten)
        return True, count[0]
    return False, 0


def collect_html_files():
    files = []
    for root, dirs, filenames in os.walk(SITE_ROOT):
        # Prune skipped directories in-place
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in filenames:
            if fname.endswith(".html") and fname not in SKIP_FILES:
                files.append(Path(root) / fname)
    return files


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    config = load_config()
    tools = config["tools"]

    # Print current status of each tool
    print("=== Affiliate config status ===")
    for slug, cfg in tools.items():
        status = f"AFFILIATE: {cfg['affiliate_url']}" if cfg["affiliate_url"] else "PENDING (using plain URL)"
        print(f"  {slug:20s} → {status}")
    print()

    html_files = collect_html_files()
    print(f"Scanning {len(html_files)} HTML files...\n")

    total_files = 0
    total_links = 0
    report = {}  # slug → list of relative file paths

    for filepath in sorted(html_files):
        changed, count = process_file(filepath, tools)
        if changed:
            total_files += 1
            total_links += count
            rel_path = str(filepath.relative_to(SITE_ROOT))
            # Attribute changes to tool slugs
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            for domain, slug in DOMAIN_MAP.items():
                if domain in content:
                    report.setdefault(slug, set()).add(rel_path)
            print(f"  ✓ {rel_path} ({count} link(s) updated)")

    print(f"\nDone. {total_links} link(s) updated across {total_files} file(s).")

    if report:
        print("\n=== Pages updated per tool ===")
        for slug, pages in sorted(report.items()):
            print(f"\n  {slug}:")
            for p in sorted(pages):
                print(f"    - {p}")


if __name__ == "__main__":
    main()
