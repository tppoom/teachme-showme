#!/usr/bin/env python3
"""Inline a real image into a deck as a data: URI (the deck must stay one file).

Usage:  python3 embed-image.py <image> ["alt text"] [--full]

Prints a ready-to-paste block: a <figure class="fig"> by default, or a full-bleed
imgfull slide body with --full. Warns above 600 KB — a slide image that large wants
cropping, not embedding.

There is no placeholder mode here on purpose: if you don't have the image, ship the
honest .ph block from layouts.html rather than something that looks like evidence.
"""
import sys, base64, pathlib, mimetypes, html

if len(sys.argv) < 2: sys.exit(__doc__)
src = pathlib.Path(sys.argv[1])
alt = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else src.stem
full = "--full" in sys.argv
mime = mimetypes.guess_type(src.name)[0] or "image/png"
if not mime.startswith("image/"): sys.exit(f"not an image: {mime}")
b64 = base64.b64encode(src.read_bytes()).decode()
kb = len(b64) / 1024
if kb > 600:
    print(f"<!-- WARNING: {kb:.0f} KB inlined from {src.name}. Crop or downscale it. -->", file=sys.stderr)
uri = f"data:{mime};base64,{b64}"
a = html.escape(alt)
if full:
    print(f'<img src="{uri}" alt="{a}">\n<div class="ovl"></div>\n'
          f'<div class="cap"><h2>Headline that states the claim</h2>\n'
          f'  <p class="lead">One line of context.</p></div>')
else:
    print(f'<figure class="fig"><img src="{uri}" alt="{a}">\n'
          f'  <figcaption>{a}</figcaption></figure>')
print(f"embedded {src.name}: {src.stat().st_size/1024:.0f} KB -> {kb:.0f} KB base64", file=sys.stderr)
