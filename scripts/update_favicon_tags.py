#!/usr/bin/env python3
"""
Update favicon <link> tags in all HTML files to include the full
multi-size favicon set (16, 32, 192, 512, apple-touch-icon).

The script detects the correct relative path prefix based on file depth.
It replaces any existing favicon/icon link tags in the <head> and inserts
the correct set.
"""

import os
import re
import glob

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# New canonical favicon block — uses {prefix} placeholder for relative paths
FAVICON_BLOCK_TEMPLATE = """\
  <link rel="icon" type="image/x-icon" href="{prefix}favicon.ico" />
  <link rel="icon" type="image/png" sizes="16x16" href="{prefix}favicon-16.png" />
  <link rel="icon" type="image/png" sizes="32x32" href="{prefix}favicon-32.png" />
  <link rel="icon" type="image/png" sizes="192x192" href="{prefix}favicon-192.png" />
  <link rel="icon" type="image/png" sizes="512x512" href="{prefix}favicon-512.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="{prefix}apple-touch-icon.png" />"""

# Pattern to match existing favicon/icon link tags (all variants)
FAVICON_PATTERN = re.compile(
    r'\s*<link\s[^>]*rel="(?:icon|shortcut icon|apple-touch-icon)"[^>]*/>\s*',
    re.IGNORECASE
)

def get_prefix(html_path):
    """Return the relative path prefix from the HTML file back to site root."""
    rel = os.path.relpath(SITE_ROOT, os.path.dirname(html_path))
    if rel == '.':
        return ''
    return rel.replace('\\', '/') + '/'

def update_file(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file has any favicon tags
    if not FAVICON_PATTERN.search(content):
        # No favicon tags at all — skip template/fragment files
        return False, "no favicon tags found — skipped"

    prefix = get_prefix(html_path)
    new_block = FAVICON_BLOCK_TEMPLATE.format(prefix=prefix)

    # Remove all existing favicon link tags
    cleaned = FAVICON_PATTERN.sub('', content)

    # Insert new block after <head> opening tag or after charset meta
    # Find the best insertion point: after <meta charset...> or after <head>
    insert_after = re.search(
        r'(<meta\s+charset[^>]+>|<meta\s+name="viewport"[^>]+>)',
        cleaned, re.IGNORECASE
    )
    if insert_after:
        pos = insert_after.end()
        new_content = cleaned[:pos] + '\n' + new_block + cleaned[pos:]
    else:
        # Fallback: insert after <head>
        head_match = re.search(r'<head[^>]*>', cleaned, re.IGNORECASE)
        if head_match:
            pos = head_match.end()
            new_content = cleaned[:pos] + '\n' + new_block + cleaned[pos:]
        else:
            return False, "no <head> tag found — skipped"

    if new_content == content:
        return False, "no changes needed"

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, f"updated (prefix: '{prefix}')"

# Find all HTML files
html_files = glob.glob(os.path.join(SITE_ROOT, '**', '*.html'), recursive=True)
html_files = [f for f in html_files if 'node_modules' not in f]
html_files.sort()

updated = 0
skipped = 0

for path in html_files:
    rel_path = os.path.relpath(path, SITE_ROOT)
    changed, msg = update_file(path)
    status = "✓" if changed else "–"
    print(f"  {status} {rel_path}: {msg}")
    if changed:
        updated += 1
    else:
        skipped += 1

print(f"\nDone: {updated} files updated, {skipped} skipped.")
