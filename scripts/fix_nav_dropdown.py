#!/usr/bin/env python3
"""
Inject ct-nav dropdown CSS into all deep-dive pages that use compare-template.css
but are missing the dropdown rules (since compare-template.css has no .dropdown styles).
"""

import re
from pathlib import Path

PAGES = [
    "analytics-tools-saas-founders-2026/index.html",
    "support-stack-saas-founders-2026/index.html",
    "billing-stack-saas-founders-2026/index.html",
    "automation-stack-agencies-2026/index.html",
]

DROPDOWN_CSS = """
    /* ── Nav dropdown (ct-nav) ── */
    .ct-nav li.has-dropdown {
      position: relative;
    }
    .ct-nav li.has-dropdown > a::after {
      content: " \\25BE";
      font-size: 0.7em;
      opacity: 0.55;
      margin-left: 0.1em;
    }
    .ct-nav .dropdown {
      display: none;
      position: absolute;
      top: calc(100% + 6px);
      left: 0;
      min-width: 220px;
      background: #fff;
      border: 1px solid var(--ct-border, #e5e7eb);
      border-radius: 6px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.10);
      z-index: 200;
      padding: 0.35rem 0;
      flex-direction: column;
      gap: 0;
      list-style: none;
    }
    .ct-nav li.has-dropdown:hover > .dropdown,
    .ct-nav li.has-dropdown:focus-within > .dropdown {
      display: flex;
    }
    .ct-nav .dropdown li {
      width: 100%;
    }
    .ct-nav .dropdown a {
      display: block;
      padding: 0.5rem 1rem;
      font-size: 0.875rem;
      white-space: nowrap;
      color: var(--ct-text, #111827);
      text-decoration: none;
    }
    .ct-nav .dropdown a:hover {
      background: var(--ct-bg-alt, #f9fafb);
      color: var(--ct-accent-a, #2563eb);
    }
"""

site_root = Path(__file__).parent.parent

for page_path in PAGES:
    full_path = site_root / page_path
    content = full_path.read_text(encoding="utf-8")

    # Skip if already patched
    if ".ct-nav .dropdown" in content:
        print(f"SKIP (already patched): {page_path}")
        continue

    # Insert before closing </style> tag
    if "</style>" not in content:
        print(f"WARN: no </style> found in {page_path}")
        continue

    # Insert the dropdown CSS just before the first </style>
    patched = content.replace("  </style>", DROPDOWN_CSS + "  </style>", 1)
    full_path.write_text(patched, encoding="utf-8")
    print(f"PATCHED: {page_path}")

print("Done.")
