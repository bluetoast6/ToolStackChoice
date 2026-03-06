#!/usr/bin/env python3
"""
Generate a complete favicon set from logo-icon.png.
Outputs:
  favicon.ico          — multi-size ICO (16, 32, 48px)
  favicon-16.png       — 16x16 PNG
  favicon-32.png       — 32x32 PNG (replaces favicon.png)
  favicon-48.png       — 48x48 PNG
  favicon-192.png      — 192x192 PNG (Android Chrome / Google favicon cache)
  favicon-512.png      — 512x512 PNG (PWA / high-res aggregators)
  apple-touch-icon.png — 180x180 PNG (already exists, regenerate for quality)
"""

import os
from PIL import Image

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(SITE_ROOT, "logo-icon.png")

sizes = {
    "favicon-16.png":       16,
    "favicon-32.png":       32,
    "favicon-48.png":       48,
    "favicon-192.png":      192,
    "favicon-512.png":      512,
    "apple-touch-icon.png": 180,
}

src = Image.open(SOURCE).convert("RGBA")
print(f"Source image: {SOURCE} — {src.size}")

for filename, size in sizes.items():
    out_path = os.path.join(SITE_ROOT, filename)
    img = src.resize((size, size), Image.LANCZOS)
    img.save(out_path, "PNG", optimize=True)
    print(f"  ✓ {filename} ({size}x{size})")

# Also overwrite favicon.png (32x32) for backward compat
favicon_png = os.path.join(SITE_ROOT, "favicon.png")
src.resize((32, 32), Image.LANCZOS).save(favicon_png, "PNG", optimize=True)
print(f"  ✓ favicon.png (32x32) — updated")

# Generate multi-size .ico (16, 32, 48)
ico_path = os.path.join(SITE_ROOT, "favicon.ico")
ico_images = [
    src.resize((16, 16), Image.LANCZOS),
    src.resize((32, 32), Image.LANCZOS),
    src.resize((48, 48), Image.LANCZOS),
]
ico_images[0].save(
    ico_path,
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48)],
    append_images=ico_images[1:],
)
print(f"  ✓ favicon.ico (16/32/48px multi-size)")

print("\nAll favicon files generated successfully.")
