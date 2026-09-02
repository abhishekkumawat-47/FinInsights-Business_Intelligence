"""The cover, rendered as one full-bleed A4 image.

Drawing it rather than laying it out in Word buys exact control of the gradient, the tracking and
the optical margins, and it removes the single most common way a .docx breaks on someone else's
machine: a cover that reflows onto two pages.

The gradient is the dashboard's own `--hero-grad`, sampled at the same five stops.
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch

import theme as T

for _f in (T.FONT_REGULAR, T.FONT_BOLD, T.FONT_ITALIC, T.FONT_BOLDITALIC):
    font_manager.fontManager.addfont(_f)
plt.rcParams["font.family"] = "Archivo"

# --hero-grad: 105deg, #3d12c9 → #4a19d4 → #4e1bda → #6d28e6 → #8b3af0
HERO = LinearSegmentedColormap.from_list(
    "hero", [(0.00, "#3D12C9"), (0.38, "#4A19D4"), (0.62, "#4E1BDA"),
             (0.88, "#6D28E6"), (1.00, "#8B3AF0")])


def _gradient(ax, w, h):
    """The hero gradient at ~105 degrees, i.e. mostly horizontal with a slight rise."""
    n = 900
    x = np.linspace(0, 1, n)
    y = np.linspace(0, 1, n)
    xx, yy = np.meshgrid(x, y)
    t = np.clip(0.86 * xx + 0.30 * yy - 0.08, 0, 1)
    ax.imshow(HERO(t), extent=(0, w, 0, h), aspect="auto", origin="lower", zorder=0,
              interpolation="bilinear")
    # a magenta bloom in the upper-right corner, as in the reference designs
    r = np.sqrt((xx - 1.05) ** 2 + (yy - 1.10) ** 2)
    glow = np.clip(1 - r / 0.85, 0, 1) ** 2
    rgba = np.zeros((n, n, 4))
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = 0.78, 0.32, 0.98
    rgba[..., 3] = glow * 0.55
    ax.imshow(rgba, extent=(0, w, 0, h), aspect="auto", origin="lower", zorder=1,
              interpolation="bilinear")


def _wave(ax, w, h):
    """A quiet contour motif so the field is not a flat rectangle."""
    xs = np.linspace(-0.1, 1.1, 600)
    for i in range(7):
        phase = i * 0.42
        amp = 0.030 + i * 0.004
        base = 0.055 + i * 0.026
        ys = base + amp * np.sin(xs * 5.1 + phase) + 0.018 * np.sin(xs * 11.0 + phase * 1.7)
        ax.plot(xs * w, ys * h, color="white", lw=0.9, alpha=0.11 - i * 0.008, zorder=2)


def render(path, meta):
    w, h = 21.0, 29.7
    fig = plt.figure(figsize=(w / 2.54, h / 2.54), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    _gradient(ax, w, h)
    _wave(ax, w, h)

    M = 3.0  # the cover's optical margin, matching the body text block

    # ── masthead ─────────────────────────────────────────────────────────────
    ax.add_patch(FancyBboxPatch((M, h - 3.30), 0.62, 0.62,
                                boxstyle="round,pad=0,rounding_size=0.16",
                                facecolor="white", edgecolor="none", zorder=4))
    ax.plot([M + 0.19, M + 0.19], [h - 3.10, h - 2.86], color=T.BRAND_STRONG, lw=2.0,
            solid_capstyle="round", zorder=5)
    ax.plot([M + 0.31, M + 0.31], [h - 3.10, h - 2.74], color=T.BRAND_STRONG, lw=2.0,
            solid_capstyle="round", zorder=5)
    ax.plot([M + 0.43, M + 0.43], [h - 3.10, h - 2.94], color=T.BRAND_MAGENTA, lw=2.0,
            solid_capstyle="round", zorder=5)
    ax.text(M + 0.86, h - 2.90, "FinInsights", fontsize=15, color="white", fontweight="bold",
            va="center", zorder=5)
    ax.text(w - M, h - 2.90, meta["eyebrow"], fontsize=8.4, color="white", alpha=0.80,
            va="center", ha="right", zorder=5)
    ax.plot([M, w - M], [h - 3.72, h - 3.72], color="white", alpha=0.28, lw=0.8, zorder=4)

    # ── title block ──────────────────────────────────────────────────────────
    ax.text(M, 21.15, meta["kicker"], fontsize=9.0, color="#E9DDFF", fontweight="bold",
            va="bottom", zorder=5, alpha=0.95)
    ax.text(M, 20.55, meta["title"], fontsize=40, color="white", fontweight="bold", va="top",
            linespacing=1.08, zorder=5)
    ax.text(M, 14.35, meta["subtitle"], fontsize=14.0, color="#EFE7FF", va="top",
            linespacing=1.42, zorder=5)

    # ── the three claims the document has to defend ──────────────────────────
    cy = 8.55
    ax.plot([M, w - M], [cy + 1.55, cy + 1.55], color="white", alpha=0.28, lw=0.8, zorder=4)
    colw = (w - 2 * M) / 3
    for i, (big, small) in enumerate(meta["claims"]):
        x = M + i * colw
        ax.text(x, cy + 0.85, big, fontsize=12.5, color="white", fontweight="bold", va="center",
                zorder=5)
        ax.text(x, cy + 0.22, small, fontsize=7.6, color="#DCCFFA", va="top", linespacing=1.45,
                zorder=5)

    # ── footer ───────────────────────────────────────────────────────────────
    ax.plot([M, w - M], [4.05, 4.05], color="white", alpha=0.28, lw=0.8, zorder=4)
    ax.text(M, 3.40, meta["team"], fontsize=10.5, color="white", fontweight="bold", va="top",
            zorder=5)
    ax.text(M, 2.78, meta["org"], fontsize=8.8, color="#DCCFFA", va="top", linespacing=1.45,
            zorder=5)
    ax.text(w - M, 3.40, meta["date"], fontsize=8.8, color="#DCCFFA", va="top", ha="right",
            zorder=5)
    ax.text(w - M, 2.86, meta["doctype"], fontsize=8.8, color="white", va="top", ha="right",
            zorder=5)

    fig.savefig(path, dpi=300, facecolor="none")
    plt.close(fig)
    return path
