"""Measure every page's trailing whitespace and flag the ones that read as a mistake.

A ragged page bottom is normal. A page that stops eight centimetres short of the margin because a
heading and its figure could not fit together is not — it reads as a layout accident. This finds
those pages so they can be fixed by reflowing content rather than by eye.
"""
from __future__ import annotations

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pymupdf

PDF = sys.argv[1] if len(sys.argv) > 1 else "FinInsights_Business_Proposal.pdf"
CM = 28.3465                      # points per centimetre
BOTTOM_MARGIN = 2.15 * CM
LIMIT = float(sys.argv[2]) if len(sys.argv) > 2 else 4.5   # cm of tolerated trailing white

doc = pymupdf.open(PDF)
page_h = doc[0].rect.height
foot_top = page_h - BOTTOM_MARGIN - 0.9 * CM   # ignore the running footer

worst = []
for i, pg in enumerate(doc, 1):
    if i == 1:
        continue
    lowest = 0.0
    for b in pg.get_text("blocks"):
        x0, y0, x1, y1, txt = b[0], b[1], b[2], b[3], b[4]
        if y0 > foot_top:                       # the footer itself
            continue
        if not txt.strip():
            continue
        lowest = max(lowest, y1)
    for img in pg.get_image_info():
        r = img["bbox"]
        if r[3] < foot_top:
            lowest = max(lowest, r[3])
    for d in pg.get_drawings():                 # table rules and panel fills
        r = d["rect"]
        if r.y1 < foot_top:
            lowest = max(lowest, r.y1)
    gap = (page_h - BOTTOM_MARGIN - lowest) / CM
    worst.append((gap, i))

worst.sort(reverse=True)
print(f"{doc.page_count} pages")
bad = [(g, p) for g, p in worst if g > LIMIT]
for g, p in worst[:12]:
    flag = "  <-- fix" if g > LIMIT else ""
    print(f"  page {p:>2}  trailing white {g:5.1f} cm{flag}")
print(f"\n{len(bad)} page(s) over {LIMIT} cm")
