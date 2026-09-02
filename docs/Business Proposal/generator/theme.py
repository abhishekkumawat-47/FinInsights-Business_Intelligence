"""One palette and one typeface for the whole proposal, taken from dashboard/src/app/globals.css.

The document is meant to read as the same product as the dashboard, so nothing here is chosen by
eye: every hex is copied from the stylesheet, and the typeface is the same Archivo the app loads
through next/font.
"""
from __future__ import annotations

import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONT_DIR = os.path.join(ROOT, "fonts", "static")
FIG_DIR = os.path.join(HERE, "figs")

# ── Brand ────────────────────────────────────────────────────────────────────
BRAND = "#5B21E0"
BRAND_STRONG = "#4014CC"
BRAND_DEEP = "#2D0B96"
BRAND_BRIGHT = "#7C3AED"
BRAND_MAGENTA = "#A855F7"
BRAND_SOFT = "#F1ECFE"
BRAND_LINE = "#E4DBFB"

# ── Rails (near-black) ───────────────────────────────────────────────────────
RAIL = "#0B0A12"
RAIL_RAISED = "#16141F"
RAIL_LINE = "#23202F"

# ── Warm-shifted neutrals (the redefined slate scale) ────────────────────────
N50 = "#FAF8FD"
N100 = "#F3EFF9"
N200 = "#E8E2F1"
N300 = "#D3CAE3"
N400 = "#8D86A1"
N500 = "#6C6581"
N600 = "#4B4661"
N700 = "#342F49"
N800 = "#201C34"
N900 = "#141020"

SURFACE = "#FFFFFF"
SUNKEN = "#FAFAFD"
HAIRLINE = "#ECECF3"

# ── Direction / semantics ────────────────────────────────────────────────────
RISE = "#0F9D76"
FALL = "#F82768"
WARN = "#E8912A"

# Categorical ramp for charts: brand-led, then the two accents, then neutrals.
# Ordered so the first three are distinguishable in greyscale as well as colour.
SERIES = [BRAND_DEEP, BRAND_BRIGHT, BRAND_MAGENTA, "#5EC8D8", N400, N300]

# Engine tags, used wherever the LLM/non-LLM split is drawn.
ENGINE = {
    "sql": BRAND_DEEP,
    "stats": BRAND,
    "rules": BRAND_BRIGHT,
    "ml": BRAND_MAGENTA,
    "llm": WARN,
}

FONT_REGULAR = os.path.join(FONT_DIR, "Archivo-Regular.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "Archivo-Bold.ttf")
FONT_ITALIC = os.path.join(FONT_DIR, "Archivo-Italic.ttf")
FONT_BOLDITALIC = os.path.join(FONT_DIR, "Archivo-BoldItalic.ttf")
