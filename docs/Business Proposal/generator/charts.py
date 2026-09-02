"""Every figure in the proposal, drawn once from one palette.

Authored at the width they are placed at (W inches == the 15 cm text column), so nothing is
rescaled on the page and a 8 pt label in a figure is a 8 pt label in the document. That is the
whole trick to a document with no font-size drift.

House rules: no chart frame, no legend where a direct label will do, one grid direction at most,
values written on the mark, and the interpretation left to the caption so the figure stays quiet.
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

import theme as T

for _f in (T.FONT_REGULAR, T.FONT_BOLD, T.FONT_ITALIC, T.FONT_BOLDITALIC):
    font_manager.fontManager.addfont(_f)

W = 5.91  # inches == 15 cm, the text column

plt.rcParams.update({
    "font.family": "Archivo",
    "font.size": 8.0,
    "text.color": T.N700,
    "axes.edgecolor": T.N300,
    "axes.labelcolor": T.N600,
    "xtick.color": T.N500,
    "ytick.color": T.N500,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

os.makedirs(T.FIG_DIR, exist_ok=True)


def _save(fig, name):
    path = os.path.join(T.FIG_DIR, name + ".png")
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    print("  " + name)
    return path


def _tag(ax, text, colour=None, x=0.0, y=1.0):
    """A small provenance pill.

    A chart of invented numbers that looks like a chart of measured numbers is the exact failure
    the product exists to prevent, so every figure says what kind of thing it is.
    """
    ax.text(x, y, text, transform=ax.transAxes, ha="left", va="bottom", fontsize=6.2,
            color=colour or T.N400, fontweight="bold")


def _bare(ax, keep=()):
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(side in keep)
    for side in keep:
        ax.spines[side].set_color(T.N300)
        ax.spines[side].set_linewidth(0.7)


# ─────────────────────────────────────────────────────────────────────────────
# 01 · Where the six hours of an investigation actually go
# ─────────────────────────────────────────────────────────────────────────────
def fig_analyst_day():
    steps = [
        ("Verify the number and reconcile sources", 2.2, T.BRAND_DEEP, "machine"),
        ("Segment down to a driver", 1.6, T.BRAND, "machine"),
        ("Check history and known events", 1.0, T.BRAND_BRIGHT, "machine"),
        ("Assemble the evidence trail", 0.7, T.BRAND_MAGENTA, "machine"),
        ("Write the summary the business reads", 0.5, T.WARN, "human"),
    ]
    fig, ax = plt.subplots(figsize=(W, 2.05))
    for i, (label, hours, colour, kind) in enumerate(steps):
        y = len(steps) - 1 - i
        ax.barh(y, hours, height=0.50, color=colour)
        ax.text(hours + 0.09, y, f"{hours:.1f} h", va="center", fontsize=8.0,
                fontweight="bold", color=colour)
        ax.text(-0.12, y, label, va="center", ha="right", fontsize=7.6, color=T.N700)
    ax.plot([2.95, 2.95], [0.72, 4.28], color=T.N300, lw=0.8)
    ax.text(3.05, 2.5, "5.5 of the 6 hours is reconstruction:\nmechanical, repeatable, and the "
                       "part a\ndeterministic engine does faster and\nwith a permanent audit trail",
            va="center", fontsize=7.4, color=T.N500, linespacing=1.45)
    ax.text(3.05, 0.0, "0.5 h. The only artefact\nthe business actually reads",
            va="center", fontsize=7.4, color=T.WARN, linespacing=1.45, fontweight="bold")
    ax.set_xlim(0, 6.4)
    ax.set_ylim(-0.62, 4.62)
    ax.set_xticks([])
    ax.set_yticks([])
    _bare(ax)
    _tag(ax, "MODELLED FROM THE ASSUMPTIONS STATED IN SECTION 8.4")
    _save(fig, "01_analyst_day")


# ─────────────────────────────────────────────────────────────────────────────
# 02 · The determinism boundary
# ─────────────────────────────────────────────────────────────────────────────
def fig_engine_boundary():
    stages = [
        ("01", "Contract", "sql"), ("02", "Trust\nGate", "rules"), ("03", "Detect", "stats"),
        ("04", "Localize", "stats"), ("05", "Forecast", "stats"), ("06", "Causal", "stats"),
        ("07", "Decide", "rules"), ("08", "Narrate", "llm"),
    ]
    fig, ax = plt.subplots(figsize=(W, 2.30))
    bw, gap = 1.00, 0.13
    for i, (num, name, eng) in enumerate(stages):
        x = i * (bw + gap)
        colour = T.ENGINE[eng]
        ax.add_patch(FancyBboxPatch((x, 0.72), bw, 0.66,
                                    boxstyle="round,pad=0.0,rounding_size=0.07",
                                    facecolor=colour, edgecolor="none"))
        ax.text(x + bw / 2, 1.22, num, ha="center", va="center", color="white", fontsize=6.6,
                alpha=0.72)
        ax.text(x + bw / 2, 0.98, name, ha="center", va="center", color="white", fontsize=7.6,
                fontweight="bold", linespacing=1.15)
        ax.text(x + bw / 2, 0.55, eng.upper(), ha="center", va="center", color=colour,
                fontsize=6.5, fontweight="bold")

    span = 7 * (bw + gap) + bw
    det_w = 7 * (bw + gap) - gap / 2
    ax.add_patch(Rectangle((-0.09, 0.42), det_w + 0.09, 1.06, facecolor="none",
                           edgecolor=T.BRAND_DEEP, linewidth=1.0, linestyle=(0, (3.5, 2))))
    ax.text(det_w / 2, 1.68, "DETERMINISTIC  ·  every number computed and stored here",
            ha="center", va="center", fontsize=7.6, fontweight="bold", color=T.BRAND_DEEP)
    ax.add_patch(Rectangle((det_w + 0.055, 0.42), bw + 0.13, 1.06, facecolor="none",
                           edgecolor=T.WARN, linewidth=1.0, linestyle=(0, (3.5, 2))))
    ax.text(det_w + 0.62, 1.68, "MODEL" + chr(10) + "phrases only", ha="center", va="center",
            fontsize=7.6, fontweight="bold", color=T.WARN, linespacing=1.35)

    ax.add_patch(FancyBboxPatch((-0.09, -0.02), span + 0.18, 0.34,
                                boxstyle="round,pad=0.0,rounding_size=0.06",
                                facecolor=T.BRAND_SOFT, edgecolor=T.BRAND_LINE, linewidth=0.7))
    ax.text(span / 2, 0.15, "SIGNAL STORE  ·  every figure stored with its engine tag, inputs "
                            "hash, latency and cost",
            ha="center", va="center", fontsize=7.3, color=T.BRAND_DEEP)
    ax.text(span / 2, -0.36, "The narrator reads only this store. It never sees a raw event, and "
                             "the verifier re-checks every\nfigure it writes back against the row "
                             "the figure came from.",
            ha="center", va="center", fontsize=7.3, color=T.N500, linespacing=1.45)
    ax.set_xlim(-0.22, span + 0.32)
    ax.set_ylim(-0.62, 1.88)
    ax.axis("off")
    _tag(ax, "FROM THE BUILD", y=0.97)
    _save(fig, "02_engine_boundary")


# ─────────────────────────────────────────────────────────────────────────────
# 03 · The KPI chain
# ─────────────────────────────────────────────────────────────────────────────
def fig_kpi_chain():
    fig, ax = plt.subplots(figsize=(W, 2.30))
    bw, bh = 1.62, 0.66
    nodes = [
        ("New account\nsignups", 0.0, "COUNT", T.BRAND_BRIGHT),
        ("KYC completion\nrate", 1.98, "RATE", T.BRAND),
        ("Loan approval\nvolume", 3.96, "COUNT", T.BRAND),
        ("Revenue", 5.94, "MONEY", T.BRAND_DEEP),
    ]
    for label, x, shape, colour in nodes:
        ax.add_patch(FancyBboxPatch((x, 1.30), bw, bh,
                                    boxstyle="round,pad=0.0,rounding_size=0.07",
                                    facecolor=colour, edgecolor="none"))
        ax.text(x + bw / 2, 1.70, label, ha="center", va="center", color="white", fontsize=7.9,
                fontweight="bold", linespacing=1.2)
        ax.text(x + bw / 2, 1.44, shape, ha="center", va="center", color="white", fontsize=6.4,
                alpha=0.78)
    for x0 in (1.62, 3.60, 5.58):
        ax.add_patch(FancyArrowPatch((x0 + 0.04, 1.63), (x0 + 0.32, 1.63), arrowstyle="-|>",
                                     mutation_scale=10, color=T.N400, lw=1.1))

    fx = 3.15
    ax.add_patch(FancyBboxPatch((fx, 0.24), bw, bh, boxstyle="round,pad=0.0,rounding_size=0.07",
                                facecolor=T.FALL, edgecolor="none"))
    ax.text(fx + bw / 2, 0.64, "Transaction\nfailure rate", ha="center", va="center",
            color="white", fontsize=7.9, fontweight="bold", linespacing=1.2)
    ax.text(fx + bw / 2, 0.38, "RATE", ha="center", va="center", color="white", fontsize=6.4,
            alpha=0.78)
    for tx in (2.60, 4.60, 6.60):
        ax.add_patch(FancyArrowPatch((fx + bw / 2, 0.94), (tx, 1.26), arrowstyle="-|>",
                                     mutation_scale=9, color=T.FALL, lw=0.95,
                                     linestyle=(0, (3, 2)), alpha=0.9,
                                     connectionstyle="arc3,rad=-0.16"))
    ax.text(fx + bw / 2, 0.02, "can drag any of the four down", ha="center", va="top",
            fontsize=7.2, color=T.FALL)
    ax.text(0.0, 2.14, "explained by segment and time", fontsize=7.1, color=T.N500)
    ax.text(2.30, 2.31, "explained on the two counts beneath it, never on the rate",
            fontsize=7.1, color=T.N500)
    ax.text(5.94, 2.14, "explained by fee line and\nby the volume driver upstream",
            fontsize=7.1, color=T.N500, linespacing=1.4)
    ax.set_xlim(-0.12, 8.15)
    ax.set_ylim(-0.30, 2.80)
    ax.axis("off")
    _tag(ax, "FROM THE BUILD", y=0.97)
    _save(fig, "03_kpi_chain")


# ─────────────────────────────────────────────────────────────────────────────
# 04 · Reference architecture
# ─────────────────────────────────────────────────────────────────────────────
def fig_architecture():
    fig, ax = plt.subplots(figsize=(W, 3.30))
    LEFT, RIGHT = 0.0, 9.40

    def band(y, h, label, colour, tint):
        ax.add_patch(FancyBboxPatch((LEFT, y), RIGHT, h,
                                    boxstyle="round,pad=0.0,rounding_size=0.06",
                                    facecolor=tint, edgecolor=T.N200, linewidth=0.7))
        ax.text(LEFT - 0.16, y + h / 2, label, ha="right", va="center", rotation=90,
                fontsize=6.9, fontweight="bold", color=colour)

    def box(x, y, w, h, label, sub="", fill="white", fg=None, edge=None, fs=7.4):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.06",
                                    facecolor=fill, edgecolor=edge or T.N300, linewidth=0.8))
        ax.text(x + w / 2, y + (h * 0.63 if sub else h / 2), label, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=fg or T.N800, linespacing=1.15)
        if sub:
            ax.text(x + w / 2, y + h * 0.27, sub, ha="center", va="center", fontsize=6.3,
                    color=fg or T.N500)

    cols = [0.12, 2.42, 4.72, 7.02]
    cw = 2.20

    band(4.28, 0.98, "SOURCES", T.N500, T.N50)
    box(cols[0], 4.47, cw, 0.60, "NexaBank core", "daily snapshot")
    box(cols[1], 4.47, cw, 0.60, "Clickstream", "per event, Kafka")
    box(cols[2], 4.47, cw, 0.60, "Simulate panel", "plants it first")
    box(cols[3], 4.47, cw, 0.60, "Ground truth", "fixture file")

    band(3.02, 1.06, "PLATFORM", T.BRAND, T.BRAND_SOFT)
    box(cols[0], 3.25, cw, 0.60, "Ingestion API", "mask · dedupe")
    box(cols[1], 3.25, cw, 0.60, "Bronze", "raw, append-only")
    box(cols[2], 3.25, cw, 0.60, "Silver", "canonical, one day")
    box(cols[3], 3.25, cw, 0.60, "Gold", "rollups · cube")

    band(1.02, 1.86, "INTELLIGENCE", T.BRAND_DEEP, "#F7F4FE")
    box(0.12, 2.32, 9.10, 0.44, "Metric API  ·  the only doorway into the warehouse", "",
        fill=T.BRAND_DEEP, fg="white", edge=T.BRAND_DEEP, fs=7.2)
    box(0.12, 1.76, 9.10, 0.44,
        "Trust Gate → Detect → Localize → Forecast → Causal → Decide", "", fs=7.2)
    box(0.12, 1.10, 2.86, 0.56, "Signal Store", "findings, on Gold", fs=7.2)
    box(3.24, 1.10, 2.86, 0.56, "Narrator", "small local model", fill="#FDF6EC", edge=T.WARN,
        fs=7.2)
    box(6.36, 1.10, 2.86, 0.56, "Numeric verifier", "no trace, no number", fill="#FDF6EC",
        edge=T.WARN, fs=7.2)

    band(0.06, 0.90, "DELIVERY", T.N500, T.N50)
    box(cols[0], 0.22, cw, 0.58, "Dashboard", "KPI · funnel", fs=6.9)
    box(cols[1], 0.22, cw, 0.58, "Evidence card", "freshness · lineage", fs=6.9)
    box(cols[2], 0.22, cw, 0.58, "Engine breakdown", "read from records", fs=6.9)
    box(cols[3], 0.22, cw, 0.58, "Human approval", "human in the loop", fs=6.9)

    for c in cols:
        ax.add_patch(FancyArrowPatch((c + cw / 2, 4.45), (c + cw / 2, 3.87), arrowstyle="-|>",
                                     mutation_scale=9, color=T.N400, lw=0.9))
    ax.add_patch(FancyArrowPatch((1.22, 3.23), (1.22, 2.80), arrowstyle="-|>", mutation_scale=9,
                                 color=T.N400, lw=0.9))
    fb = 9.60
    ax.plot([9.22, fb], [0.51, 0.51], color=T.RISE, lw=1.0, ls=(0, (3, 2)))
    ax.plot([fb, fb], [0.51, 1.38], color=T.RISE, lw=1.0, ls=(0, (3, 2)))
    ax.add_patch(FancyArrowPatch((fb, 1.38), (9.25, 1.38), arrowstyle="-|>", mutation_scale=9,
                                 color=T.RISE, lw=1.0, ls=(0, (3, 2))))
    ax.text(fb + 0.14, 1.14, "feedback:\nthe outcome is\nwritten back\nagainst the\nfinding that\n"
                             "proposed it", ha="left", va="center", fontsize=6.4, color=T.RISE,
            linespacing=1.4)
    ax.set_xlim(-0.62, 11.30)
    ax.set_ylim(-0.02, 5.42)
    ax.axis("off")
    _tag(ax, "FROM THE BUILD", y=0.985)
    _save(fig, "04_architecture")


# ─────────────────────────────────────────────────────────────────────────────
# 05 · Detect
# ─────────────────────────────────────────────────────────────────────────────
def fig_detect_band():
    days = list(range(1, 29))
    base = [812, 798, 826, 840, 805, 690, 645, 830, 818, 844, 851, 822, 700, 651,
            836, 829, 848, 812, 833, 705, 660, 841, 827, 618, 560, 534, 690, 648]
    expected = [(842 if d % 7 not in (6, 0) else 672) for d in days]
    lo = [e * 0.905 for e in expected]
    hi = [e * 1.095 for e in expected]
    fig, ax = plt.subplots(figsize=(W, 2.00))
    ax.fill_between(days, lo, hi, color=T.BRAND_SOFT, edgecolor=T.BRAND_LINE, linewidth=0.7)
    ax.plot(days, base, color=T.BRAND_DEEP, lw=1.5, zorder=3)
    flagged = [24, 25, 26]
    ax.plot(flagged, [base[d - 1] for d in flagged], "o", ms=4.6, color=T.FALL,
            markeredgecolor="white", markeredgewidth=0.9, zorder=4)
    ax.annotate("fires only when a move is unlikely," + chr(10) + "material and persistent",
                xy=(25.2, 528), xytext=(18.6, 404), fontsize=7.2, color=T.FALL,
                arrowprops=dict(arrowstyle="-|>", color=T.FALL, lw=0.9), linespacing=1.4)
    ax.annotate("weekend dips sit inside the band," + chr(10) + "because seasonality belongs "
                "in the baseline",
                xy=(13, 706), xytext=(1.0, 404), fontsize=7.2, color=T.N500,
                arrowprops=dict(arrowstyle="-|>", color=T.N400, lw=0.8), linespacing=1.4)
    ax.text(28.9, 842, "forecast band\nfrom stage 04", fontsize=7.0, color=T.BRAND, va="center",
            linespacing=1.4)
    ax.set_ylim(320, 990)
    ax.set_xlim(0.4, 34.5)
    ax.set_xticks([1, 7, 14, 21, 28])
    ax.set_xticklabels(["day 1", "7", "14", "21", "28"], fontsize=7.2)
    ax.set_yticks([500, 700, 900])
    ax.tick_params(length=0, labelsize=7.2)
    ax.grid(axis="y", color=T.HAIRLINE, lw=0.7)
    ax.set_axisbelow(True)
    _bare(ax)
    _tag(ax, "ILLUSTRATIVE. THE RULE, NOT MEASURED OUTPUT", colour=T.WARN)
    _save(fig, "05_detect_band")


# ─────────────────────────────────────────────────────────────────────────────
# 06 · Contribution waterfall
# ─────────────────────────────────────────────────────────────────────────────
def fig_waterfall():
    start = 100.0
    steps = [
        ("KYC leak\nmobile, tier-2", -8.6, T.FALL),
        ("Transaction\nfailures", -4.1, T.FALL),
        ("Signup\nmix", -1.5, T.FALL),
        ("Unexplained\nresidual", -1.0, T.N400),
    ]
    fig, ax = plt.subplots(figsize=(W, 2.20))
    ax.bar(0, start, width=0.52, color=T.BRAND_DEEP)
    ax.text(0, start + 2.2, "100.0", ha="center", fontsize=8.0, fontweight="bold", color=T.N800)
    ax.text(0, -4.5, "Revenue\nbaseline", ha="center", va="top", fontsize=7.2, color=T.N600,
            linespacing=1.35)
    running = start
    for i, (label, delta, colour) in enumerate(steps, start=1):
        bottom = running + delta
        ax.bar(i, -delta, bottom=bottom, width=0.52, color=colour)
        ax.plot([i - 0.72, i - 0.26], [running, running], color=T.N300, lw=0.7, zorder=0)
        ax.text(i, bottom - 2.4, f"{delta:+.1f}", ha="center", va="top", fontsize=8.0,
                fontweight="bold", color=colour)
        ax.text(i, -4.5, label, ha="center", va="top", fontsize=7.2, color=T.N600,
                linespacing=1.35)
        running = bottom
    n = len(steps) + 1
    ax.bar(n, running, width=0.52, color=T.BRAND)
    ax.plot([n - 0.72, n - 0.26], [running, running], color=T.N300, lw=0.7, zorder=0)
    ax.text(n, running + 2.2, f"{running:.1f}", ha="center", fontsize=8.0, fontweight="bold",
            color=T.N800)
    ax.text(n, -4.5, "Observed\nrevenue", ha="center", va="top", fontsize=7.2, color=T.N600,
            linespacing=1.35)
    ax.text(2.5, 114, "93% of the movement is attributed to a named segment; the remaining 7% is "
                      "reported\nas unexplained rather than quietly absorbed into the largest "
                      "driver",
            ha="center", va="center", fontsize=7.2, color=T.N500, linespacing=1.45)
    ax.set_ylim(-16, 124)
    ax.set_xlim(-0.7, 5.7)
    ax.set_xticks([])
    ax.set_yticks([])
    _bare(ax)
    _tag(ax, "ILLUSTRATIVE. THE METHOD, NOT MEASURED OUTPUT", colour=T.WARN)
    _save(fig, "06_waterfall")


# ─────────────────────────────────────────────────────────────────────────────
# 07 · Sparse history
# ─────────────────────────────────────────────────────────────────────────────
def fig_sparse_fan():
    hist = [42, 61, 58, 77, 71, 88, 84, 96, 91]
    fut = list(range(9, 17))
    centre = [91, 93, 95, 97, 99, 101, 103, 105]
    wide_lo = [91, 71, 63, 56, 50, 45, 41, 37]
    wide_hi = [91, 118, 131, 143, 155, 167, 179, 192]
    tight_lo = [91, 88, 86, 85, 84, 83, 82, 81]
    tight_hi = [91, 99, 104, 109, 113, 117, 121, 125]
    fig, ax = plt.subplots(figsize=(W, 1.98))
    ax.fill_between(fut, wide_lo, wide_hi, color=T.BRAND_SOFT, edgecolor=T.BRAND_LINE, lw=0.8)
    ax.fill_between(fut, tight_lo, tight_hi, color="#FDECF2", edgecolor=T.FALL, lw=0.8,
                    linestyle=(0, (3, 2)), alpha=0.6)
    ax.plot(fut, centre, color=T.BRAND, lw=1.1, linestyle=(0, (4, 2)))
    ax.plot(range(1, 10), hist, color=T.BRAND_DEEP, lw=1.6, marker="o", ms=3.0,
            markeredgecolor="white", markeredgewidth=0.7)
    ax.axvline(9, color=T.N300, lw=0.8)
    ax.text(8.8, 33, "9 days of history", fontsize=7.1, color=T.N500, ha="right")
    ax.text(16.6, 162, "what the engine returns:\na wide, explicitly caveated range",
            fontsize=7.2, color=T.BRAND_DEEP, va="center", linespacing=1.4, fontweight="bold")
    ax.text(16.6, 88, "what a confident point estimate\nwould have claimed instead",
            fontsize=7.2, color=T.FALL, va="center", linespacing=1.4)
    ax.text(0.9, 205, "Student travel card · activations per day", fontsize=7.1, color=T.N500)
    ax.set_xlim(0.4, 27.0)
    ax.set_ylim(20, 222)
    ax.set_xticks([1, 5, 9, 13, 16])
    ax.set_xticklabels(["launch", "d5", "today", "d13", "d16"], fontsize=7.2)
    ax.set_yticks([50, 100, 150])
    ax.tick_params(length=0, labelsize=7.2)
    ax.grid(axis="y", color=T.HAIRLINE, lw=0.7)
    ax.set_axisbelow(True)
    _bare(ax)
    _tag(ax, "ILLUSTRATIVE. THE METHOD, NOT MEASURED OUTPUT", colour=T.WARN)
    _save(fig, "07_sparse_fan")


# ─────────────────────────────────────────────────────────────────────────────
# 08 · Run economics
# ─────────────────────────────────────────────────────────────────────────────
def fig_observe_record(fields, stages):
    """What Observe writes for every stage of every run.

    An earlier draft of this figure showed stage latencies in milliseconds. Those numbers were
    invented, and presenting invented numbers as measured telemetry is precisely the failure this
    product exists to prevent, so the figure now shows the record instead of fictional values in
    it. The column names are taken from the Signal Store schema.
    """
    fig, ax = plt.subplots(figsize=(W, 2.15))
    x = 0.0
    for name, eng in stages:
        colour = T.ENGINE[eng]
        ax.add_patch(FancyBboxPatch((x, 1.62), 1.06, 0.34,
                                    boxstyle="round,pad=0.0,rounding_size=0.06",
                                    facecolor=colour, edgecolor="none"))
        ax.text(x + 0.53, 1.79, name, ha="center", va="center", color="white", fontsize=6.6,
                fontweight="bold")
        ax.add_patch(FancyArrowPatch((x + 0.53, 1.58), (x + 0.53, 1.32), arrowstyle="-|>",
                                     mutation_scale=7, color=T.N300, lw=0.8))
        x += 1.19

    span = x - 0.13
    ax.add_patch(FancyBboxPatch((0.0, 0.14), span, 1.16,
                                boxstyle="round,pad=0.0,rounding_size=0.06",
                                facecolor=T.N50, edgecolor=T.BRAND_LINE, linewidth=0.8))
    ax.text(span / 2, 1.18, "one row written per stage, per run",
            ha="center", va="center", fontsize=7.0, color=T.BRAND_DEEP, fontweight="bold")
    cols = 3
    for i, (col, meaning) in enumerate(fields):
        cx = 0.28 + (i % cols) * (span / cols)
        cy = 0.92 - (i // cols) * 0.30
        ax.text(cx, cy, col, ha="left", va="center", fontsize=6.6, color=T.N800,
                fontweight="bold", family="monospace")
        ax.text(cx, cy - 0.125, meaning, ha="left", va="center", fontsize=6.1, color=T.N500)

    ax.text(0.0, 0.02, "Cost per insight is therefore a figure the customer can watch, not a "
                       "number we assert. It is not quoted here" + chr(10) + "because this "
                       "prototype has not been run at production volume.",
            ha="left", va="top", fontsize=6.9, color=T.N500, linespacing=1.45)
    ax.set_xlim(-0.1, span + 0.1)
    ax.set_ylim(-0.42, 2.10)
    ax.axis("off")
    _tag(ax, "SCHEMA, FROM THE BUILD", y=0.96)
    _save(fig, "08_observe_record")


# ─────────────────────────────────────────────────────────────────────────────
# 09 · The value floor
# ─────────────────────────────────────────────────────────────────────────────
def fig_value_floor(rows):
    fig, ax = plt.subplots(figsize=(W, 2.00))
    labels = [r[0] for r in rows][::-1]
    lows = [r[1] for r in rows][::-1]
    highs = [r[2] for r in rows][::-1]
    kinds = [r[3] for r in rows][::-1]
    for i, (lo, hi, kind) in enumerate(zip(lows, highs, kinds)):
        colour = T.BRAND_DEEP if kind == "sourced" else T.BRAND_BRIGHT
        ax.plot([lo, hi], [i, i], color=colour, lw=5.5, solid_capstyle="round", alpha=0.28)
        ax.plot([lo, hi], [i, i], color=colour, lw=1.4, solid_capstyle="butt")
        ax.plot([lo, hi], [i, i], "|", color=colour, ms=8, mew=1.5)
        ax.text(hi + 5, i, f"${lo}–{hi}K", va="center", fontsize=7.3, color=T.N600)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=7.4)
    ax.set_xlim(0, max(highs) * 1.38)
    ax.set_xticks([0, 50, 100, 150, 200])
    ax.set_xticklabels(["$0", "$50K", "$100K", "$150K", "$200K"], fontsize=7.1)
    ax.tick_params(length=0)
    ax.grid(axis="x", color=T.HAIRLINE, lw=0.7)
    ax.set_axisbelow(True)
    _bare(ax)
    _tag(ax, "MODELLED. EACH ASSUMPTION IS STATED IN 8.1")
    _save(fig, "09_value_floor")


# ─────────────────────────────────────────────────────────────────────────────
# 10 · Payback
# ─────────────────────────────────────────────────────────────────────────────
def fig_payback():
    months = list(range(0, 13))
    cost = [38, 52, 63, 72, 80, 87, 94, 101, 108, 115, 122, 129, 136]
    value = [0, 6, 22, 48, 82, 121, 163, 208, 255, 304, 355, 408, 462]
    fig, ax = plt.subplots(figsize=(W, 1.95))
    ax.axvspan(3, 5, color=T.BRAND_SOFT, zorder=0)
    ax.fill_between(months, cost, value, where=[v > c for v, c in zip(value, cost)],
                    color=T.RISE, alpha=0.11, zorder=1)
    ax.plot(months, cost, color=T.N500, lw=1.4, linestyle=(0, (4, 2)), zorder=2)
    ax.plot(months, value, color=T.BRAND_DEEP, lw=1.8, zorder=3)
    ax.text(12.3, 462, "cumulative value", fontsize=7.3, color=T.BRAND_DEEP, va="center",
            fontweight="bold")
    ax.text(12.3, 136, "cumulative cost", fontsize=7.3, color=T.N500, va="center")
    ax.text(4, 372, "crossover\nmonths 3–5", ha="center", fontsize=7.4, color=T.BRAND,
            fontweight="bold", linespacing=1.4)
    ax.set_xlim(0, 17.6)
    ax.set_ylim(0, 505)
    ax.set_xticks([0, 3, 6, 9, 12])
    ax.set_xticklabels(["month 0", "3", "6", "9", "12"], fontsize=7.1)
    ax.set_yticks([0, 150, 300, 450])
    ax.set_yticklabels(["$0", "$150K", "$300K", "$450K"], fontsize=7.1)
    ax.tick_params(length=0)
    ax.grid(axis="y", color=T.HAIRLINE, lw=0.7)
    ax.set_axisbelow(True)
    _bare(ax)
    _tag(ax, "MODELLED")
    _save(fig, "10_payback")


# ─────────────────────────────────────────────────────────────────────────────
# 11 · The readiness gap
# ─────────────────────────────────────────────────────────────────────────────
def fig_ai_gap(bars, caption, footnote):
    """Two figures from one survey, which is the only honest way to put them side by side."""
    fig, ax = plt.subplots(figsize=(W, 1.80))
    for i, (labelling, v, colour) in enumerate(bars):
        y = len(bars) - 1 - i
        ax.barh(y, v, color=colour, height=0.30)
        ax.text(v + 1.8, y, f"{v}%", va="center", fontsize=14, fontweight="bold", color=colour)
        ax.text(0, y + 0.30, labelling, va="bottom", ha="left", fontsize=8.4, color=T.N800,
                fontweight="bold")
    ax.text(0, len(bars) - 0.30, caption, va="bottom", ha="left", fontsize=7.4, color=T.N500)
    ax.text(0, -0.62, footnote, va="top", ha="left", fontsize=7.0, color=T.N500, linespacing=1.45)
    ax.set_xlim(0, 100)
    ax.set_ylim(-1.15, len(bars) + 0.05)
    ax.set_xticks([])
    ax.set_yticks([])
    _bare(ax)
    _save(fig, "11_ai_gap")


# ─────────────────────────────────────────────────────────────────────────────
# 12 · Risk, inherent to residual
# ─────────────────────────────────────────────────────────────────────────────
def fig_risk(rows):
    """Inherent score, the control, residual score, as a value axis, not two columns.

    Labelling the two ends INHERENT and RESIDUAL would be wrong: both are positions on the same
    1-to-5 severity scale, and which one sits left depends on the risk. The key says which dot is
    which instead.
    """
    fig, ax = plt.subplots(figsize=(W, 2.35))
    n = len(rows)
    for i, (rid, label, inh, res) in enumerate(rows[::-1]):
        ax.plot([inh, res], [i, i], color=T.N300, lw=0.9, zorder=1)
        ax.add_patch(FancyArrowPatch((inh, i), (res + (0.10 if res < inh else -0.10), i),
                                     arrowstyle="-|>", mutation_scale=8, color=T.N400, lw=0.9,
                                     zorder=1))
        for val, colour in ((inh, T.FALL), (res, T.RISE)):
            ax.plot(val, i, "o", ms=8.0, color=colour, markeredgecolor="white",
                    markeredgewidth=0.9, zorder=3)
            ax.text(val, i, str(val), ha="center", va="center", fontsize=6.2, color="white",
                    fontweight="bold", zorder=4)
        ax.text(0.55, i, rid, ha="right", va="center", fontsize=7.3, color=T.N500,
                fontweight="bold")
        ax.text(5.55, i, label, ha="left", va="center", fontsize=7.3, color=T.N700)

    key_y = n - 0.34
    ax.plot(0.95, key_y, "o", ms=6.5, color=T.FALL, markeredgecolor="white", markeredgewidth=0.8)
    ax.text(1.20, key_y, "inherent", va="center", fontsize=6.7, color=T.FALL, fontweight="bold")
    ax.plot(3.30, key_y, "o", ms=6.5, color=T.RISE, markeredgecolor="white", markeredgewidth=0.8)
    ax.text(3.55, key_y, "residual, once the control is in place", va="center", fontsize=6.7,
            color=T.RISE, fontweight="bold")
    ax.text(10.60, key_y, "severity 1 (low) to 5", va="center", fontsize=6.7, color=T.N400)
    ax.set_xlim(0.0, 15.6)
    ax.set_ylim(-0.7, n + 0.05)
    ax.set_xticks([])
    ax.set_yticks([])
    _bare(ax)
    _tag(ax, "OUR ASSESSMENT, NOT A MEASUREMENT")
    _save(fig, "12_risk")


# ─────────────────────────────────────────────────────────────────────────────
# 13 · Roadmap
# ─────────────────────────────────────────────────────────────────────────────
def fig_roadmap(phases):
    """Phase name at the left, bar on the timeline, scope aligned in one column at the right.

    Putting the label inside the bar fails as soon as one phase is short: a three-month bar has no
    room for the words. A left-hand label works at any duration.
    """
    fig, ax = plt.subplots(figsize=(W, 1.95))
    TEXT_X = 20.0
    for i, (name, start_m, end_m, colour, scope, gate) in enumerate(phases):
        y = 2 - i
        ax.add_patch(FancyBboxPatch((start_m, y - 0.15), end_m - start_m, 0.30,
                                    boxstyle="round,pad=0.0,rounding_size=0.10",
                                    facecolor=colour, edgecolor="none"))
        ax.text(-0.9, y, name, ha="right", va="center", color=colour, fontsize=7.6,
                fontweight="bold")
        ax.text(TEXT_X, y + 0.09, scope, ha="left", va="center", fontsize=7.0, color=T.N700)
        ax.text(TEXT_X, y - 0.13, "gate · " + gate, ha="left", va="center", fontsize=6.6,
                color=T.N500)
    for m in (0, 3, 9, 18):
        ax.plot([m, m], [-0.28, 2.52], color=T.HAIRLINE, lw=0.8, zorder=0)
        ax.text(m, -0.46, str(m), ha="center", fontsize=6.9, color=T.N500)
    ax.text(-0.9, -0.46, "months", ha="right", fontsize=6.9, color=T.N500)
    ax.set_xlim(-9.5, 49)
    ax.set_ylim(-0.80, 2.72)
    ax.axis("off")
    _save(fig, "13_roadmap")
