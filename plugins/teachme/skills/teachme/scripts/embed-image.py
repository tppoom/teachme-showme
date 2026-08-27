#!/usr/bin/env python3
"""Inline a local image into a course as a data: URI (the file must stay self-contained).

Usage:  python3 embed-image.py <image> [caption] >> parts/07-ui.html

Emits a ready-to-paste <figure class="viz"> block. Warns above 400 KB — a screenshot
that large usually wants cropping, not embedding.
"""
import sys, base64, pathlib, mimetypes, html

if len(sys.argv) < 2: sys.exit(__doc__)
src = pathlib.Path(sys.argv[1])
cap = sys.argv[2] if len(sys.argv) > 2 else ""
mime = mimetypes.guess_type(src.name)[0] or "image/png"
if not mime.startswith("image/"): sys.exit(f"not an image: {mime}")
raw = src.read_bytes()
b64 = base64.b64encode(raw).decode()
kb = len(b64) / 1024
if kb > 400:
    print(f"<!-- WARNING: {kb:.0f} KB inlined from {src.name}. Crop or downscale it. -->", file=sys.stderr)
print(f'<figure class="viz">\n'
      f'<img src="data:{mime};base64,{b64}" alt="{html.escape(cap or src.stem)}" '
      f'style="max-width:100%;height:auto;border-radius:9px;border:1px solid var(--line)">\n'
      f'<figcaption>{html.escape(cap)}</figcaption>\n</figure>')
print(f"embedded {src.name}: {len(raw)/1024:.0f} KB -> {kb:.0f} KB base64", file=sys.stderr)
