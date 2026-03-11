#!/usr/bin/env python3
"""Quick QA: print all affiliate-tracked links found in the site."""
import re, pathlib, json

SITE_ROOT = pathlib.Path(__file__).parent.parent
CONFIG_FILE = SITE_ROOT / "affiliates.json"
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

config = json.loads(CONFIG_FILE.read_text())
tools = config["tools"]

for fpath in sorted(SITE_ROOT.rglob("*.html")):
    content = fpath.read_text(encoding="utf-8")
    tags = re.findall(r'<a\b[^>]*href="https?://[^"]*(?:' +
                      "|".join(re.escape(d) for d in DOMAIN_MAP) +
                      r')[^"]*"[^>]*>', content)
    if not tags:
        continue
    print(f"\n{fpath.relative_to(SITE_ROOT)}")
    for t in tags:
        href = re.search(r'href="([^"]+)"', t)
        rel  = re.search(r'rel="([^"]+)"', t)
        tgt  = 'target="_blank"' in t
        print(f"  href={href.group(1) if href else 'NONE':<55} rel={rel.group(1) if rel else 'NONE':<25} target_blank={tgt}")
