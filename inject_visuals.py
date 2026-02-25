#!/usr/bin/env python3
"""
inject_visuals.py
Injects visuals.css link + purposeful visual components into each review
and comparison page. Idempotent: skips pages already patched.
"""

import re, pathlib

BASE = pathlib.Path("/home/ubuntu/toolreview-site")

# ── helpers ──────────────────────────────────────────────────────────────────

def add_css_link(html: str, filename: str) -> str:
    """Add <link rel="stylesheet" href="visuals.css"> after style.css link."""
    if "visuals.css" in html:
        return html  # already patched
    return html.replace(
        '<link rel="stylesheet" href="style.css" />',
        '<link rel="stylesheet" href="style.css" />\n  <link rel="stylesheet" href="visuals.css" />'
    )

def insert_after(html: str, anchor: str, snippet: str) -> str:
    """Insert snippet immediately after the first occurrence of anchor."""
    if snippet.strip()[:30] in html:
        return html  # already present
    idx = html.find(anchor)
    if idx == -1:
        return html
    insert_at = idx + len(anchor)
    return html[:insert_at] + snippet + html[insert_at:]

# ── visual snippets ───────────────────────────────────────────────────────────

def tool_badge(icon_class: str, name: str, tagline: str) -> str:
    return f"""
          <!-- Visual: tool identity badge -->
          <figure class="tool-badge" role="img" aria-label="{name} — {tagline}">
            <div class="tool-badge__icon tool-badge__icon--{icon_class}" aria-hidden="true">{name[:2].upper()}</div>
            <figcaption class="tool-badge__text">
              <p class="tool-badge__name">{name}</p>
              <p class="tool-badge__tagline">{tagline}</p>
            </figcaption>
          </figure>
"""

def score_chart(rows: list[tuple[str,float,str]]) -> str:
    """rows = [(label, value_0_to_5, display_str), ...]"""
    items = ""
    for label, val, disp in rows:
        pct = round(val / 5 * 100, 1)
        items += f"""
            <div class="score-chart__row">
              <span class="score-chart__label">{label}</span>
              <div class="score-chart__bar-track" role="presentation">
                <div class="score-chart__bar-fill" style="width:{pct}%" aria-hidden="true"></div>
              </div>
              <span class="score-chart__value">{disp}</span>
            </div>"""
    return f"""
          <!-- Visual: score bar chart -->
          <figure class="score-chart" aria-label="Score breakdown bar chart" loading="lazy">
            {items}
            <figcaption class="score-chart__caption">Scores out of 5 — see full scorecard above for methodology.</figcaption>
          </figure>
"""

def vs_diagram(icon_a: str, name_a: str, score_a: str, best_a: str,
               icon_b: str, name_b: str, score_b: str, best_b: str) -> str:
    return f"""
          <!-- Visual: A vs B comparison diagram -->
          <figure class="vs-diagram" role="img"
            aria-label="{name_a} vs {name_b} — at-a-glance scores and best-fit summary">
            <div class="vs-diagram__side vs-diagram__side--a">
              <div class="vs-diagram__icon vs-diagram__icon--{icon_a}" aria-hidden="true">{name_a[:2].upper()}</div>
              <p class="vs-diagram__name">{name_a}</p>
              <p class="vs-diagram__score">{score_a}</p>
              <p class="vs-diagram__score-label">out of 5</p>
              <p class="vs-diagram__best-for">{best_a}</p>
            </div>
            <div class="vs-diagram__divider" aria-hidden="true">VS</div>
            <div class="vs-diagram__side vs-diagram__side--b">
              <div class="vs-diagram__icon vs-diagram__icon--{icon_b}" aria-hidden="true">{name_b[:2].upper()}</div>
              <p class="vs-diagram__name">{name_b}</p>
              <p class="vs-diagram__score">{score_b}</p>
              <p class="vs-diagram__score-label">out of 5</p>
              <p class="vs-diagram__best-for">{best_b}</p>
            </div>
          </figure>
"""

# ── per-page definitions ──────────────────────────────────────────────────────

PAGES = [
    {
        "file": "make-com-review.html",
        "css_anchor": '<link rel="stylesheet" href="style.css" />',
        "badge": tool_badge("make", "Make.com", "Visual no-code automation platform"),
        "badge_anchor": '<h2 id="what-is">What is Make.com?</h2>',
        "chart": score_chart([
            ("Ease of use",       4.0, "4.0"),
            ("Feature depth",     5.0, "5.0"),
            ("Pricing fairness",  5.0, "5.0"),
            ("Reliability",       4.0, "4.0"),
            ("Support quality",   4.0, "4.0"),
        ]),
        "chart_anchor": '<div class="scorecard" role="region" aria-label="Review summary scorecard">',
    },
    {
        "file": "n8n-cloud-review.html",
        "css_anchor": '<link rel="stylesheet" href="style.css" />',
        "badge": tool_badge("n8n", "n8n Cloud", "Developer-friendly open-source automation"),
        "badge_anchor": '<h2 id="what-is">What is n8n Cloud?</h2>',
        "chart": score_chart([
            ("Ease of use",       3.5, "3.5"),
            ("Feature depth",     4.9, "4.9"),
            ("Pricing fairness",  4.3, "4.3"),
            ("Reliability",       4.6, "4.6"),
            ("Support quality",   4.1, "4.1"),
        ]),
        "chart_anchor": '<div class="scorecard" role="region" aria-label="Review summary scorecard">',
    },
    {
        "file": "ahrefs-review.html",
        "css_anchor": '<link rel="stylesheet" href="style.css" />',
        "badge": tool_badge("ahrefs", "Ahrefs", "Industry-leading SEO and backlink analysis platform"),
        "badge_anchor": '<h2 id="what-is">What is Ahrefs?</h2>',
        "chart": score_chart([
            ("Ease of use",              4.0, "4.0"),
            ("Feature depth",            4.8, "4.8"),
            ("Pricing fairness",         3.6, "3.6"),
            ("Reliability / data",       4.7, "4.7"),
            ("Support & learning",       4.5, "4.5"),
        ]),
        "chart_anchor": '<div class="scorecard" role="region" aria-label="Review summary scorecard">',
    },
    {
        "file": "semrush-review.html",
        "css_anchor": '<link rel="stylesheet" href="style.css" />',
        "badge": tool_badge("semrush", "Semrush", "All-in-one digital marketing and SEO platform"),
        "badge_anchor": '<h2 id="what-is">What is Semrush?</h2>',
        "chart": score_chart([
            ("Ease of use",              4.0, "4.0"),
            ("Feature depth",            4.9, "4.9"),
            ("Pricing fairness",         3.5, "3.5"),
            ("Reliability / data",       4.7, "4.7"),
            ("Support & learning",       4.6, "4.6"),
        ]),
        "chart_anchor": '<div class="scorecard" role="region" aria-label="Review summary scorecard">',
    },
    {
        "file": "hostinger-review.html",
        "css_anchor": '<link rel="stylesheet" href="style.css" />',
        "badge": tool_badge("hostinger", "Hostinger", "Budget-friendly web hosting with hPanel"),
        "badge_anchor": '<h2 id="what-is">What is Hostinger?</h2>',
        "chart": score_chart([
            ("Ease of use",              4.7, "4.7"),
            ("Feature depth",            4.0, "4.0"),
            ("Pricing fairness",         4.6, "4.6"),
            ("Reliability / perf.",      4.1, "4.1"),
            ("Support & learning",       3.9, "3.9"),
        ]),
        "chart_anchor": '<div class="scorecard" role="region" aria-label="Review summary scorecard">',
    },
    {
        "file": "siteground-review.html",
        "css_anchor": '<link rel="stylesheet" href="style.css" />',
        "badge": tool_badge("siteground", "SiteGround", "Premium managed hosting on Google Cloud"),
        "badge_anchor": '<h2 id="what-is">What is SiteGround?</h2>',
        "chart": score_chart([
            ("Ease of use",              4.4, "4.4"),
            ("Feature depth",            4.3, "4.3"),
            ("Pricing fairness",         3.8, "3.8"),
            ("Reliability / perf.",      4.7, "4.7"),
            ("Support & learning",       4.6, "4.6"),
        ]),
        "chart_anchor": '<div class="scorecard" role="region" aria-label="Review summary scorecard">',
    },
]

COMPARISON_PAGES = [
    {
        "file": "make-vs-n8n-cloud.html",
        "diagram": vs_diagram(
            "make",    "Make.com",  "4.6", "Best for visual workflow builders",
            "n8n",     "n8n Cloud", "4.4", "Best for developers & power users",
        ),
        "diagram_anchor": '<h2 id="ct-quick"',
    },
    {
        "file": "ahrefs-vs-semrush.html",
        "diagram": vs_diagram(
            "ahrefs",  "Ahrefs",   "4.4", "Best for SEO & backlink analysis",
            "semrush", "Semrush",  "4.5", "Best for multi-channel marketing",
        ),
        "diagram_anchor": '<h2 id="ct-quick"',
    },
    {
        "file": "hostinger-vs-siteground.html",
        "diagram": vs_diagram(
            "hostinger",  "Hostinger",  "4.3", "Best for budget-conscious sites",
            "siteground", "SiteGround", "4.4", "Best for managed WordPress",
        ),
        "diagram_anchor": '<h2 id="ct-quick"',
    },
]

# ── main ──────────────────────────────────────────────────────────────────────

changed = []

for page in PAGES:
    path = BASE / page["file"]
    html = path.read_text(encoding="utf-8")

    html = add_css_link(html, page["file"])

    # Insert score chart BEFORE the scorecard div
    html = insert_after(html, page["chart_anchor"], page["chart"])

    # Insert tool badge AFTER the h2 "What is…" opening tag
    # Find the closing > of that h2 line
    m = re.search(re.escape(page["badge_anchor"]), html)
    if m:
        end = html.find("</h2>", m.start()) + len("</h2>")
        if page["badge"].strip()[:30] not in html:
            html = html[:end] + page["badge"] + html[end:]

    path.write_text(html, encoding="utf-8")
    changed.append(page["file"])
    print(f"  patched: {page['file']}")

for page in COMPARISON_PAGES:
    path = BASE / page["file"]
    html = path.read_text(encoding="utf-8")

    html = add_css_link(html, page["file"])

    # Insert VS diagram BEFORE the h2 quick-comparison heading
    anchor = page["diagram_anchor"]
    m = re.search(re.escape(anchor), html)
    if m and page["diagram"].strip()[:30] not in html:
        html = html[:m.start()] + page["diagram"] + html[m.start():]

    path.write_text(html, encoding="utf-8")
    changed.append(page["file"])
    print(f"  patched: {page['file']}")

print(f"\nDone. {len(changed)} files patched.")
