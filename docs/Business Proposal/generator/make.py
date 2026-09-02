"""Build the proposal: figures, then the document, then embed the fonts."""
from __future__ import annotations

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import charts
import cover
import theme as T
import embed_fonts
from docx import Document
from docx.enum.section import WD_SECTION
from docx.shared import Pt

import docx_kit as K
import content_a as A
import content_b as B
import content_c as C

OUT = sys.argv[1] if len(sys.argv) > 1 else "FinInsights_Business_Proposal.docx"

# ── figures ──────────────────────────────────────────────────────────────────
print("figures")
cover.render("figs/00_cover.png", dict(
    eyebrow="Accenture Innovation Challenge 2026  ·  Round 2",
    kicker="BUSINESSINTELLIGENCE.AI",
    title="The decision layer\nyour dashboards\nnever had",
    subtitle="A KPI intelligence-to-action engine for retail banking, in which\n"
             "the language model never produces a number.",
    claims=[
        ("Five KPIs, one chain",
         "Signups, KYC completion, loan\napprovals, revenue and failures\nexplained as one story"),
        ("No LLM arithmetic",
         "Every figure is computed by a\ndeterministic tool, stored, and\nre-verified before it "
         "ships"),
        ("It is allowed to refuse",
         "Abstention is a designed output\nwith its own artefact, not a\nfailure mode"),
    ],
    team="Team Nexus",
    org="Indian Institute of Technology, Patna",
    date="September 2026",
    doctype="Detailed business proposal"))
print("  00_cover")

charts.fig_analyst_day()
charts.fig_engine_boundary()
charts.fig_kpi_chain()
charts.fig_architecture()
charts.fig_detect_band()
charts.fig_waterfall()
charts.fig_sparse_fan()
charts.fig_observe_record(
    fields=[("investigation_id", "which run"), ("stage", "which tool"),
            ("engine_type", "sql, stats, rules, ml or llm"), ("inputs_hash", "reproducibility"),
            ("latency_ms", "wall clock"), ("tokens_in / tokens_out", "model calls, if any"),
            ("cost_est_usd", "priced at the serving rate"), ("verifier_pass", "did every figure trace"),
            ("rows_scanned", "how much of the cube was searched")],
    stages=[("Trust Gate", "rules"), ("Detect", "stats"), ("Localize", "stats"),
            ("Forecast", "stats"), ("Causal", "stats"), ("Decide", "rules"),
            ("Narrate", "llm")])
charts.fig_value_floor([
    ("Analyst time reclaimed", 140, 190, "sourced"),
    ("Avoided bad decisions", 120, 160, "modelled"),
    ("Licence recovery", 50, 100, "modelled"),
    ("Reporting cycles", 25, 40, "modelled"),
])
charts.fig_payback()
charts.fig_ai_gap(
    bars=[("Use AI to write the code that produces the numbers", 72, T.BRAND_DEEP),
          ("Use AI to test, observe and check what comes out", 24, T.FALL)],
    caption="Where data teams are putting AI in their own workflow",
    footnote="The gap is the opportunity. Teams have adopted AI on the production side and left "
             "the checking side alone," + chr(10) + "which is exactly the half this product "
             "automates.")
charts.fig_risk([
    ("R1", "Pilot cancelled without measurable value", 5, 2),
    ("R2", "An unsupported figure reaches a reader", 5, 1),
    ("R3", "Taxonomy drift or a simulated field read as real", 4, 2),
    ("R4", "Model risk or audit blocks deployment", 4, 2),
    ("R5", "Analysts withhold adoption", 4, 2),
    ("R6", "A restricted figure reaches the wrong reader", 4, 1),
    ("R7", "Duplicate events inflate a KPI", 3, 2),
    ("R8", "Model cost and latency creep", 3, 1),
])
charts.fig_roadmap([
    ("Phase 1", 0, 3, T.BRAND_DEEP, "Full chain live on NexaBank · 5 contracts · 3 personas",
     "corrupt batch quarantined, verifier 100%"),
    ("Phase 2", 3, 9, T.BRAND, "Feedback loop wired · more contracts · wider entitlement",
     "audit reproduces 3 historic figures"),
    ("Phase 3", 9, 18, T.BRAND_BRIGHT, "Multi-tenant scale-out · platform connectors",
     "second tenant live, no engine change"),
])

# ── document ─────────────────────────────────────────────────────────────────
print("document")
doc = Document()

normal = doc.styles["Normal"]
normal.font.name = K.FONT
normal.font.size = Pt(10.5)
normal.font.color.rgb = K.rgb(T.N700)
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.30

K.set_document_defaults(doc)
cover_sec = K.setup_full_bleed_section(doc.sections[0])
K.full_page_image(doc, "figs/00_cover.png")

body_sec = doc.add_section(WD_SECTION.NEW_PAGE)
K.setup_body_section(body_sec)
body_sec.header.is_linked_to_previous = False
body_sec.footer.is_linked_to_previous = False
K.build_header(body_sec, "FinInsights  ·  BusinessIntelligence.ai  ·  Round 2")
K.build_footer(body_sec, "Team Nexus  ·  IIT Patna")
# the cover carries no furniture of its own
cover_sec.different_first_page_header_footer = False

for fn in (A.front_matter, A.executive_brief, A.problem, A.solution,
           B.kpis, B.personas, B.evidence_scenarios, B.telemetry, B.feedback,
           C.business_case, C.roadmap, C.risks, C.measurement, C.commercial,
           C.recommendation, C.appendices):
    fn(doc)
    print("  " + fn.__name__)

doc.core_properties.title = "FinInsights: KPI intelligence-to-action for retail banking"
doc.core_properties.author = "Team Nexus, IIT Patna"
doc.core_properties.subject = "BusinessIntelligence.ai · Accenture Innovation Challenge 2026"
doc.save(OUT)

n = embed_fonts.embed(OUT, "Archivo", {
    "embedRegular": T.FONT_REGULAR,
    "embedBold": T.FONT_BOLD,
    "embedItalic": T.FONT_ITALIC,
    "embedBoldItalic": T.FONT_BOLDITALIC,
})
print(f"embedded {n} font faces")
print("wrote", os.path.abspath(OUT), os.path.getsize(OUT) // 1024, "KB")
