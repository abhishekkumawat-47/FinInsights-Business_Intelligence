"""One registry for every external claim in the proposal.

Inline citations and the reference list are generated from this dict, so the two cannot drift
apart, and a source that is not listed here cannot be cited in the text. Each entry records the
publisher, the title, the date, the URL, and a `tier` that decides how the claim is worded:

  primary    the organisation that produced the data (regulator, benchmark, peer-reviewed paper)
  survey     a named survey with a stated sample, including vendor-commissioned ones
  secondary  reported elsewhere, original not reachable; the text says so

`note` carries the caveat that must travel with the figure wherever it is used.
"""
from __future__ import annotations

SOURCES = {
    # ── the trust and verification gap ──────────────────────────────────────
    "dbt26": dict(
        org="dbt Labs",
        title="2026 State of Analytics Engineering Report",
        date="April 2026",
        url="https://www.getdbt.com/resources/state-of-analytics-engineering-2026",
        tier="survey",
        note="363 data practitioners and leaders, fielded 5 December 2025 to 1 February 2026, "
             "73% practitioners.",
    ),
    "gartner_agentic": dict(
        org="Gartner",
        title="Gartner Predicts Over 40% of Agentic AI Projects Will Be Canceled by End of 2027",
        date="25 June 2025",
        url="https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-"
            "40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027",
        tier="primary",
        note="A prediction, not a measurement. Gartner's stated basis is a January 2025 poll of "
             "3,412 webinar attendees.",
    ),
    "spglobal": dict(
        org="S&P Global Market Intelligence",
        title="AI experiences rapid adoption, but with mixed outcomes. Voice of the Enterprise: "
              "AI and Machine Learning, Use Cases 2025",
        date="2025",
        url="https://www.spglobal.com/market-intelligence/en/news-insights/research/ai-experiences"
            "-rapid-adoption-but-with-mixed-outcomes-highlights-from-vote-ai-machine-learning",
        tier="survey",
        note="1,006 midlevel and senior IT and line-of-business professionals across North "
             "America and Europe. Abandonment of most AI initiatives rose from 17% to 42% year on "
             "year, with 46% of projects scrapped between proof of concept and broad adoption.",
    ),
    "omdia_soc": dict(
        org="Microsoft and Omdia",
        title="Unify now or pay later: new research on the operational cost of a fragmented SOC "
              "(State of the SOC 2026)",
        date="17 February 2026",
        url="https://www.microsoft.com/en-us/security/blog/2026/02/17/unify-now-or-pay-later-new-"
            "research-exposes-the-operational-cost-of-a-fragmented-soc/",
        tier="primary",
        note="46% of alerts prove to be false positives and 42% go uninvestigated. This is "
             "security operations, not analytics. We cite it as the closest well-measured "
             "analogue for what a low-precision alerting surface does to the people reading it.",
    ),

    # ── why a model must not produce the number ─────────────────────────────
    "vectara": dict(
        org="Vectara",
        title="Hallucination Leaderboard (HHEM)",
        date="updated May 2026",
        url="https://github.com/vectara/hallucination-leaderboard",
        tier="primary",
        note="Measures grounded summarisation: the model is given the source text. Scored by a "
             "separate evaluation model, over 7,700 articles at temperature 0.",
    ),
    "bird": dict(
        org="BIRD-SQL",
        title="BIRD text-to-SQL benchmark leaderboard",
        date="dataset NeurIPS 2023, leaderboard maintained since",
        url="https://bird-bench.github.io/",
        tier="primary",
        note="12,751 question and SQL pairs over 95 databases totalling 33.4 GB.",
    ),
    "spider2": dict(
        org="Lei et al.",
        title="Spider 2.0: Can Language Models Resolve Real-World Enterprise Text-to-SQL "
              "Workflows?",
        date="ICLR 2025, arXiv:2411.07763",
        url="https://arxiv.org/abs/2411.07763",
        tier="primary",
        note="We cite the description of enterprise conditions, not the headline accuracy number, "
             "which the leaderboard has since moved past.",
    ),
    "numreason": dict(
        org="Srivastava, Malik, Gupta, Ganu and Roth",
        title="Evaluating LLMs' Mathematical Reasoning in Financial Document Question Answering",
        date="arXiv:2402.11194, February 2024",
        url="https://arxiv.org/abs/2402.11194",
        tier="primary",
        note="Multihiertt, FinQA and TAT-QA. Error analysis attributes 20.5% to 27.6% of failures "
             "to arithmetic rather than retrieval.",
    ),

    # ── the methods the deterministic tools implement ───────────────────────
    "psqueeze": dict(
        org="Li et al., Tsinghua, Nankai, Bizseer and China Construction Bank",
        title="Generic and Robust Localization of Multi-Dimensional Root Causes (PSqueeze)",
        date="Journal of Systems and Software, 2023",
        url="https://netman.aiops.org/wp-content/uploads/2023/05/psqueeze-jss.pdf",
        tier="primary",
        note="Evaluated on two real-world datasets with 5,400 injected faults.",
    ),
    "adtributor": dict(
        org="Bhagwan et al., Microsoft Research",
        title="Adtributor: Revenue Debugging in Advertising Systems",
        date="USENIX NSDI 2014",
        url="https://www.usenix.org/system/files/conference/nsdi14/nsdi14-paper-bhagwan.pdf",
        tier="primary",
        note="Evaluated on 128 real anomaly alerts from two weeks of production data.",
    ),
    "hotspot": dict(
        org="Sun et al., Tsinghua University and Baidu",
        title="HotSpot: Anomaly Localization for Additive KPIs with Multi-Dimensional Attributes",
        date="IEEE Access, 2018",
        url="https://netman.aiops.org/wp-content/uploads/2018/12/sunyq_IEEEAccess2018_HotSpot.pdf",
        tier="primary",
        note="Reports localisation time falling from over an hour of manual work to under 20 "
             "seconds in production at a large search engine.",
    ),
    "fdr": dict(
        org="Rebjock, Kurt, Januschowski and Callot",
        title="Online false discovery rate control for anomaly detection in time series",
        date="NeurIPS 2021, arXiv:2112.03196",
        url="https://arxiv.org/abs/2112.03196",
        tier="primary",
        note="Gives a guaranteed lower bound on precision without labelled data.",
    ),
    "glad": dict(
        org="Islam, Das, Doppa and Natarajan",
        title="GLAD: GLocalized Anomaly Detection via Human-in-the-Loop Learning",
        date="arXiv:1810.01403, October 2018",
        url="https://arxiv.org/abs/1810.01403",
        tier="primary",
        note="Analyst labels tune the weights of an ensemble of simple detectors; no retraining.",
    ),

    # ── the regulatory frame ────────────────────────────────────────────────
    "rbi_local": dict(
        org="Reserve Bank of India",
        title="Storage of Payment System Data (RBI/2017-18/153, DPSS.CO.OD No.2785)",
        date="6 April 2018",
        url="https://rbi.org.in/scripts/NotificationUser.aspx?Id=11244",
        tier="primary",
        note="Binding on scheduled commercial, cooperative, payment, small finance and local area "
             "banks under the Payment and Settlement Systems Act 2007.",
    ),
    "eu_ai_act": dict(
        org="European Union",
        title="Regulation (EU) 2024/1689 (Artificial Intelligence Act), Article 6 and Annex III",
        date="2024",
        url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
        tier="primary",
        note="Creditworthiness assessment is an Annex III high-risk use. This product makes no "
             "credit decision.",
    ),

    # ── the commercial frame ────────────────────────────────────────────────
    "fdic": dict(
        org="Federal Deposit Insurance Corporation",
        title="Quarterly Banking Profile, First Quarter 2026",
        date="May 2026",
        url="https://www.fdic.gov/quarterly-banking-profile/quarterly-banking-profile-q1-2026",
        tier="primary",
        note="4,278 insured commercial banks and savings institutions, down 60 in the quarter.",
    ),
    "zylo": dict(
        org="Zylo",
        title="2025 SaaS Management Index",
        date="January 2025",
        url="https://zylo.com/news/2025-saas-management-index",
        tier="survey",
        note="Vendor research based on Zylo's own customer telemetry.",
    ),
}


def cite(key: str) -> str:
    """The short form used inline: 'dbt Labs, April 2026'."""
    s = SOURCES[key]
    return f"{s['org']}, {s['date']}"


def url(key: str) -> str:
    return SOURCES[key]["url"]


def reference_rows(order):
    """Rows for the reference list, in the order the argument uses them."""
    rows = []
    for key in order:
        s = SOURCES[key]
        rows.append((s["org"], s["title"], s["date"], s["url"], s["tier"], s["note"]))
    return rows
