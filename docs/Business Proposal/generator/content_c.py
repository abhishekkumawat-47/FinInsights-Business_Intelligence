"""Sections 8 to 13 and the appendices."""
from __future__ import annotations

import theme as T
from sources import SOURCES, url
from docx_kit import (add_run, bullets, figure, h2, h3, label, panel, para, page_break, rich,
                      section_heading, source_line, stat_band, table)

FIG = "figs/"


# ═════════════════════════════════════════════════════════════════════════════
def business_case(doc):
    section_heading(
        doc, "Section 8", "A floor we will defend line by line",
        "The case is built as two numbers rather than one, because quoting only the larger of them "
        "would be the weaker position.")

    para(doc,
         "The floor is what we will argue for. The headline range adds two effects that are real "
         "but that we cannot bound tightly: the value of a decision taken in time, and the "
         "retention of analysts who stop spending their week on reconstruction. That range is "
         "quoted second and labelled modelled wherever it appears.")

    figure(doc, FIG + "09_value_floor.png",
           "The four mechanisms that make up the floor. Analyst time is the largest single line "
           "and the only one whose unit cost is externally anchored rather than assumed.")

    h2(doc, "Each line states its own assumption", "8.1")
    table(
        doc,
        ["Mechanism", "Derivation", "Low", "High", "Basis"],
        [
            ["Analyst time", "12 investigations a week, 5 hours reclaimed, 50 weeks, $55/hour",
             "$140K", "$190K", "Unit cost sourced"],
            ["Avoided bad decisions", "3 to 4 prevented incidents a year at about $40K each",
             "$120K", "$160K", "Modelled"],
            ["Reporting cycles", "2.5 people, 3 hours a week, 80% reduction, 50 weeks",
             "$25K", "$40K", "Modelled"],
            ["Licence recovery", "Idle entitlement de-provisioning and behaviour-justified upsell",
             "$50K", "$100K", [("Zylo 2025", {"link": url("zylo")})]],
            [[("Defensible floor", {"bold": True})], "Sum of the four mechanisms above",
             [("$335K", {"bold": True})], [("$490K", {"bold": True})], "Bottom-up"],
            ["Headline range", "Adds in-time decision value and reduced analyst churn",
             "$550K", "$950K", "Modelled"],
        ],
        widths=[20, 42, 11, 11, 16], aligns=["l", "l", "r", "r", "l"], size=9.1,
        note="Zylo's 2025 SaaS Management Index puts idle licences at 52.7% of those purchased. "
             "That anchors the licence-recovery line; the share we assume you can actually reclaim "
             "is ours.")

    h2(doc, "Payback lands between months three and five", "8.2")
    figure(doc, FIG + "10_payback.png",
           "Cumulative modelled value against cumulative cost. Value ramps from month two, the "
           "point at which the first contracts clear the Trust Gate, rather than from day one, "
           "because a contract that has not passed a gate produces nothing worth counting.")

    h2(doc, "What moves the number, and by how much", "8.3")
    para(doc,
         "Showing this is a commercial choice. A buyer who can see which assumption is "
         "load-bearing will argue about that assumption instead of dismissing the whole model.")
    table(
        doc,
        ["Driver", "Downside", "Base", "Upside", "Effect on the total"],
        [
            ["Governed metric count", "5", "10", "25", "Roughly linear on three of four lines"],
            ["Upstream data quality", "Clean", "Mixed", "Fragmented",
             "Plus or minus $60K on the bad-decision line"],
            ["Reclaimable share of a day", "60%", "85 to 90%", "92%",
             "Plus or minus $50K on the analyst line"],
            ["Roles duplicating reporting", "1 shared", "2 to 3", "4 or more",
             "Plus or minus $20K, independent of size"],
            ["Loaded analyst cost", "India, $30K", "US, $110K", "US, $150K",
             "Rescales the largest line"],
        ],
        widths=[26, 15, 13, 15, 31], aligns=["l", "c", "c", "c", "l"], size=9.1)
    para(doc,
         "The last row changes the shape of the argument rather than its size. At an India-loaded "
         "analyst cost the analyst-time mechanism shrinks by roughly two thirds, and the case has "
         "to be carried by decision quality and licence recovery instead. That is a different "
         "sale, and it is worth knowing before the meeting.")

    h2(doc, "Baseline and method", "8.4")
    para(doc,
         "The baseline institution throughout is a mid-size retail bank: 150 to 400 staff across "
         "operations, risk and analytics, a data function of 6 to 12 people, and a metric "
         "footprint comparable to the chain in section 3. Cost inputs are anchored to a US senior "
         "analyst at $110K fully loaded, about $55 an hour. Incident frequency, per-decision cost, "
         "the payback profile and the headline range are modelled from those inputs. None of them "
         "is measured at a client.")
    panel(doc, "How to use this section",
          "Every line carries one of two labels. Unit cost sourced means the unit comes from an "
          "external reference and only the volume is ours. Modelled means both are ours, stated "
          "above so you can replace them. The right way to use this business case is to run a "
          "pilot that turns the modelled lines into measured ones, which is exactly what the "
          "Phase 1 exit criterion is designed to produce.")


# ═════════════════════════════════════════════════════════════════════════════
def roadmap(doc):
    section_heading(
        doc, "Section 9", "Three phases, each gated on evidence\nrather than on a date",
        "Phase 1 is built and running today. Every phase exits on a test a sceptic could run "
        "themselves, and recommendations stay human-approved in all three without exception.")

    para(doc,
         "The shape of the plan matters as much as its content. Each phase hands the next one a "
         "proof rather than a promise, and each gate belongs to the function that would otherwise "
         "be the one to stop the programme later.")

    figure(doc, FIG + "13_roadmap.png",
           "Giving each gate to the function most likely to block the programme is what stops a "
           "gate becoming a formality.")

    table(
        doc,
        ["Phase", "Scope delivered", "Exit criterion", "Gate owner"],
        [
            [[("1, built today", {"bold": True}), ("\nmonths 0 to 3", {"colour": T.N500})],
             "The full chain live end to end on NexaBank telemetry. Five KPI contracts, the "
             "ClickHouse Signal Store, Observe on every stage, three personas.",
             "The Trust Gate quarantines a seeded corrupt batch. The verifier passes on every "
             "published figure. Analyst review completes inside 60 minutes.",
             "Head of Analytics"],
            [[("2, near term", {"bold": True}), ("\nmonths 3 to 9", {"colour": T.N500})],
             "The feedback loop wired to the outcomes table. More contracts across more sources. "
             "Readers and entitlements widened beyond the first three.",
             "Overrides recalibrate the next run. Risk or audit reproduces three historic figures "
             "from the evidence bundle alone.",
             "CRO or Model Risk"],
            [[("3, scale out", {"bold": True}), ("\nmonths 9 to 18", {"colour": T.N500})],
             "Multi-tenant scale-out. Connectors for Databricks, Snowflake, Fabric, Tableau, Qlik "
             "and Looker, native, custom or hybrid. ClickHouse stays the analytical core.",
             "A second institution live with no engine change. 25 or more contracts governed. "
             "Documented run-rate value of $500K or more.",
             "CFO or CDO"],
        ],
        widths=[13, 32, 40, 15], size=9.0, pad=5.0)

    h2(doc, "What stays out of scope, in every phase", "9.1")
    para(doc,
         "These are boundaries rather than a backlog. Each one exists because crossing it would "
         "break a claim made elsewhere in this document.")
    table(
        doc,
        ["Excluded", "Why it stays out"],
        [
            ["Automated action without human approval",
             "Every action is approved by a named person and the outcome logged. Remove that step "
             "and the regulatory posture in section 10.2 stops holding."],
            ["Self-learning recommendation ranking",
             "Overrides are captured from day one, but recalibration is designed rather than "
             "deployed. Learning must never widen a contract's lever list."],
            ["Model-driven credit or risk decisions",
             "Out of scope entirely. Decide picks from a fixed lever ontology and never invents an "
             "action, which is also what keeps the system clear of the EU AI Act's high-risk "
             "classification."],
        ],
        widths=[27, 73], size=9.1, first_bold=True)

    h2(doc, "Who owns what", "9.2")
    bullets(doc, [
        ("Product and business.  ", "KPI definitions, materiality thresholds, decision owners, "
                                    "permitted levers, acceptance scenarios."),
        ("Data and platform.  ", "Source extracts, Metric API mappings, freshness, schema "
                                 "stability, tenant isolation."),
        ("Analytics and intelligence.  ", "Stage methods, Signal Store integrity, deterministic "
                                          "output, the evaluation gates at each phase exit."),
        ("Security and governance.  ", "Identity verification, role mapping, entitlement review, "
                                       "audit policy."),
        ("Operations.  ", "Review findings, approve actions, capture outcomes, feed usefulness "
                          "signals back."),
    ])


# ═════════════════════════════════════════════════════════════════════════════
def risks(doc):
    section_heading(
        doc, "Section 10", "The three risks that would kill this\nare not technical",
        "Scored 1 to 5, inherent and residual, each with a named control and a named owner.")

    para(doc,
         "Programmes of this shape rarely fail on the mathematics. They fail because a pilot "
         "produced nothing anyone could measure, because an audit function would not sign off, or "
         "because the analysts it was built for quietly declined to use it. Those are R1, R4 and "
         "R5, and each has a control that is a product decision rather than a promise.")

    figure(doc, FIG + "12_risk.png",
           "Every risk drops at least two points once its control is in place. R5 stops at 2 "
           "rather than 1 because adoption is behavioural and cannot be closed by design alone. It "
           "is re-scored at the Phase 2 gate on observed usage.")

    table(
        doc,
        ["", "Risk", "Inh.", "Control", "Res.", "Owner"],
        [
            ["R1", "Pilot delivers no measurable change and is cancelled", "5",
             "Scope fixed to contracts already live. Value measured per contract against a "
             "pre-agreed baseline.", "2", "Champion"],
            ["R2", "The narrator states a figure the evidence does not support", "5",
             "It sees evidence bundles, never raw events. The verifier traces every figure, then "
             "regenerate, redact, template.", "1", "Engineering"],
            ["R3", "Taxonomy drift, or a simulated field read as real evidence", "4",
             "Read-time canonicalisation and pre-deploy checks. Simulated fields labelled in "
             "contract and narrative.", "2", "Data Eng"],
            ["R4", "Model risk or audit blocks deployment", "4",
             "Determinism plus a per-figure evidence bundle meets model-risk documentation "
             "expectations. No credit decisioning.", "2", "CRO"],
            ["R5", "Analysts treat it as a threat and withhold adoption", "4",
             "Positioned as review and challenge. The analyst persona exposes the full bundle. "
             "Overrides are logged and feed Phase 2.", "2", "Head of Analytics"],
            ["R6", "A restricted figure reaches the wrong reader", "4",
             "Tenant selected by application, never a query parameter. Personas resolved "
             "server-side. Row-level clause in the Metric API.", "1", "Security"],
            ["R7", "Duplicate events from at-least-once delivery inflate a KPI", "3",
             "Replay-safe aggregation, exact-distinct on every count, Bronze append-only with both "
             "timestamps preserved.", "2", "Data Eng"],
            ["R8", "Model cost and latency creep as volume grows", "3",
             "Narrator-only small-model design. Observe records tokens, latency and cost per "
             "insight. The narrator is optional.", "1", "Engineering"],
        ],
        widths=[5, 22, 8, 41, 8, 16], aligns=["l", "l", "c", "l", "c", "l"], size=8.9, pad=4.4)

    h2(doc, "The evidence behind the three that matter", "10.1")
    table(
        doc,
        ["Risk", "What the evidence says", "The control"],
        [
            ["R1 Pilot cancelled",
             [("Gartner predicts over 40% of agentic AI projects will be cancelled by the end of "
               "2027 on escalating cost, unclear value and weak risk controls (", None),
              ("Gartner, June 2025", {"link": url("gartner_agentic")}),
              ("). S&P Global's survey of 1,006 IT and business leaders found abandonment of most AI "
               "initiatives rose from 17% to 42% year on year, with 46% of projects scrapped "
               "between proof of concept and broad adoption (", None),
              ("S&P Global, 2025", {"link": url("spglobal")}), (").", None)],
             "Value is measured per governed metric against a pre-agreed baseline, and every phase "
             "gate is a test a sceptic can run."],
            ["R2 A fluent answer the data does not support",
             [("Leading text-to-SQL systems still miss about one BIRD question in five, and "
               "grounded hallucination reaches zero for no model on the Vectara leaderboard. Error "
               "analysis on financial tables attributes 20% to 28% of failures to arithmetic "
               "itself rather than retrieval (", None),
              ("arXiv:2402.11194", {"link": url("numreason")}),
              (").", None)],
             "The narrator receives typed evidence bundles only. The verifier traces every figure "
             "back to the store, then bounded regeneration, redaction, template."],
            ["R5 Adoption stalls inside the analyst function",
             "Klarna publicly reversed part of its customer service automation during 2025 and "
             "rehired human agents. The pattern is over-reach, then retrenchment, and it is worth "
             "planning around rather than assuming away.",
             "Nothing acts on its own. Human approval sits in the delivery path, every action has "
             "a named owner, and the outcome is logged."],
        ],
        widths=[19, 45, 36], size=9.0, first_bold=True,
        note="The Klarna reversal is widely reported but we have not sourced it to a company "
             "statement, so it is offered as an industry pattern rather than as a measured "
             "finding.")

    h2(doc, "Regulatory posture", "10.2")
    para(doc,
         "Two regimes matter for a product of this shape. Determinism plus a per-figure evidence "
         "bundle speaks directly to model-risk documentation expectations: the model inventory "
         "entry can point at a reproducible numeric path instead of a black box with a validation "
         "report stapled to it.")
    rich(doc, [
        ("The second is scope. Because the product makes no credit or risk decision, and Decide "
         "proposes from a fixed lever ontology with a human approving, it sits outside the EU AI "
         "Act's Annex III high-risk classification, where creditworthiness assessment appears (",
         None),
        ("Regulation (EU) 2024/1689", {"link": url("eu_ai_act"), "colour": T.BRAND}),
        ("). That is a deliberate scoping choice, not a lucky accident.", None),
    ])
    para(doc,
         "The compliance gatekeeper's real test is narrower than either regime suggests. Can risk "
         "or audit reproduce a figure published six months ago, from stored evidence alone, "
         "without asking an engineer? That is written into the Phase 2 exit criterion as a "
         "concrete test on three historic figures.")


# ═════════════════════════════════════════════════════════════════════════════
def measurement(doc):
    section_heading(
        doc, "Section 11", "What to test during a pilot",
        "Each dimension below is something you can run on your own data, not a claim you have to "
        "accept.")
    table(
        doc,
        ["Dimension", "The test"],
        [
            ["Truth", "Every narrated figure traces to a Signal Store row or a contract field. "
                      "Verifier coverage is 100%."],
            ["Reliability", "Defect scenarios are quarantined. Ambiguous ones abstain with a named "
                            "confirming check."],
            ["Detection", "The planted movement is found while normal windows stay quiet. Both "
                          "halves matter."],
            ["Localisation", "The planted segment ranks first, using additive measured dimensions "
                             "only."],
            ["Forecasting", "Every eligible KPI has a stored interval, method and caveat, or an "
                            "honest sparse-history response."],
            ["Consistency", "The same frozen rows produce byte-identical numeric output."],
            ["Governance", "No restricted KPI, and no back-computable restricted figure, reaches "
                           "an unauthorised reader."],
            ["Adoption", "Users answer supported questions without a data-team ticket, and can "
                         "identify source, window and owner."],
            ["Action", "Recommendations are contract-approved, owner-assigned and human-approved. "
                       "Outcomes are recorded."],
            ["Economics", "Observe reports tokens, latency and cost per insight. Cost per governed "
                          "metric is measured, not estimated."],
        ],
        widths=[18, 82], size=9.2, first_bold=True, zebra=True)
    panel(doc, "Measure the baseline first",
          "Capture the current investigation cycle before anything is switched on: elapsed time, "
          "analyst hours, handoffs and rework per movement. Without that measurement the value "
          "model in section 8 stays modelled forever, and a modelled number is the one a sceptic "
          "discounts.")


# ═════════════════════════════════════════════════════════════════════════════
def commercial(doc):
    section_heading(
        doc, "Section 12", "Land on one expensive decision loop",
        "The entry point is not a dashboard replacement. It is a single loop in lending and "
        "onboarding, where a delayed or untrusted answer carries a visible operational cost.")

    table(
        doc,
        ["Motion", "The offer", "The customer's proof"],
        [
            ["Land", "One tenant, three connected KPIs, one persona set",
             "Time to answer, trust verdicts and action ownership, measured against the current "
             "process"],
            ["Prove", "A controlled pilot across normal, defect, sparse and permission scenarios",
             "No unsupported figures, no entitlement leaks, correct treatment of ambiguous data"],
            ["Expand", "Finance, acquisition and product metrics through contract workshops",
             "More governed coverage without proportional engineering effort"],
            ["Scale", "Multi-tenant platform and the source connector programme",
             "A second institution onboarded through contracts and mappings, not stage rewrites"],
        ],
        widths=[12, 40, 48], size=9.1, first_bold=True)

    h2(doc, "Market sizing, with the filter stated as an assumption", "12.1")
    rich(doc, [
        ("The institution count is sourced. The contract value and the readiness filter are ours, "
         "and we say so rather than dressing them in someone else's research. The FDIC's Quarterly "
         "Banking Profile for the first quarter of 2026 reports 4,278 insured commercial banks and "
         "savings institutions, down 60 over the quarter (", None),
        ("FDIC, May 2026", {"link": url("fdic"), "colour": T.BRAND}),
        (").", None),
    ])
    table(
        doc,
        ["Tier", "Scope", "Basis", "Annual value"],
        [
            ["TAM", "4,278 FDIC-insured institutions",
             [("Sourced count", {"bold": True}), (", multiplied by a $150K assumed contract value",
                                                  None)], "$641.7M"],
            ["SAM", "About 1,070 institutions",
             [("Our assumption", {"bold": True}),
              (": roughly a quarter have the data maturity to run this within a year", None)],
             "$160.5M"],
            ["SOM year 1", "3 accounts", "Initial pilot conversions", "$0.45M"],
            ["SOM year 2", "12 accounts", "Regional bank expansion", "$1.80M"],
            ["SOM year 3", "30 accounts", "Three-year phased capture", "$4.50M"],
        ],
        widths=[13, 30, 40, 17], aligns=["l", "l", "l", "r"], size=9.1, first_bold=True,
        note="An earlier draft attributed the readiness filter to published research. We could not "
             "verify that attribution, so the filter now stands as our assumption. It is the first "
             "number to challenge, and the pilot is what would replace it.")

    h2(doc, "Why this is differentiated", "12.2")
    bullets(doc, [
        ("Against BI.  ", "It says whether a movement is credible and what to do next, not only "
                          "what happened."),
        ("Against alerting.  ", "It controls false discoveries and folds related movements into "
                                "one story instead of several alerts."),
        ("Against conversational analytics.  ", "It refuses unsupported answers, preserves the "
                                                "claim set, and applies access before narration "
                                                "rather than after."),
        ("Against bespoke consulting.  ", "Contracts and the Metric API make onboarding "
                                          "repeatable across tenants and domains."),
    ])


# ═════════════════════════════════════════════════════════════════════════════
def recommendation(doc):
    section_heading(
        doc, "Section 13", "Approve a governed pilot on the\nlending and onboarding loop")
    para(doc,
         "FinInsights has a clear product boundary and a credible wedge: make the analytics you "
         "already own trustworthy, explainable and actionable for the people who carry the "
         "decision. The architecture is already shaped for a repeatable platform. The business "
         "case is strongest when the first pilot measures a baseline rather than asking the "
         "narrative layer to prove value on its own.")
    para(doc,
         "Start where KYC completion, loan approval volume and revenue form one connected story. "
         "Add finance and acquisition metrics once the trust and entitlement workflow is proven. "
         "Use the pilot to turn the modelled lines in section 8 into measured ones: investigation "
         "time, false-positive suppression, answer adoption, recommendation acceptance and "
         "realised operational impact.")
    panel(doc, "Decision requested",
          [("Authorise a KPI-contract and source-readiness pilot for one tenant, with operations, "
            "finance, analytics and risk represented in acceptance. ", None),
           ("Phase expansion is gated by evidence quality, not by narrative fluency.",
            {"bold": True}),
           (" The Phase 1 exit criterion is that the Trust Gate quarantines a seeded corrupt "
            "batch, the numeric verifier passes on every published figure, and analyst review "
            "completes inside sixty minutes.", None)],
          accent=T.BRAND_DEEP)

    label(doc, "The team")
    table(
        doc,
        ["Member", "Institution", "Stream", "Year"],
        [
            ["Omesh Mehta, team lead", "IIT Patna", "Chemical and Biochemical Engineering", "2027"],
            ["Abhishek Kumawat", "IIT Patna", "Chemical and Biochemical Engineering", "2027"],
            ["Vinod Singh Rathore", "IIT Patna", "Mechanical Engineering", "2027"],
        ],
        widths=[32, 18, 40, 10], aligns=["l", "l", "l", "c"], size=9.2, first_bold=True)


# ═════════════════════════════════════════════════════════════════════════════
def appendices(doc):
    page_break(doc)
    section_heading(
        doc, "Appendix A", "Method register",
        "Each deterministic tool implements published work. This is the register a model-risk "
        "reviewer will ask for.")
    table(
        doc,
        ["Stage", "Method and source", "What the source establishes"],
        [
            ["Detect",
             [("Online false discovery rate control for anomaly detection in time series. "
               "Rebjock, Kurt, Januschowski and Callot, NeurIPS 2021", {"link": url("fdr")})],
             "Treating each observation as a hypothesis test and applying an online "
             "Benjamini-Hochberg family gives a guaranteed lower bound on precision without "
             "labelled data. A principled cap on false alarms, rather than a tuned threshold."],
            ["Localize",
             [("PSqueeze. Li et al., Tsinghua, Nankai, Bizseer and China Construction Bank, "
               "Journal of Systems and Software, 2023", {"link": url("psqueeze")})],
             "Outperforms prior localisation methods by at least 32.89% F1 across 5,400 injected "
             "faults, localises in about ten seconds, and proves its ripple-effect property for "
             "both additive and derived measures. First method to detect root causes lying outside "
             "the recorded cube, at 0.90 F1."],
            ["Localize",
             [("Adtributor. Bhagwan et al., Microsoft Research, USENIX NSDI 2014",
               {"link": url("adtributor")})],
             "Over 95% accuracy on 128 real production anomaly alerts, and the origin of the rule "
             "we follow that derived measures such as rates cannot be attributed the way additive "
             "measures can."],
            ["Localize",
             [("HotSpot. Sun et al., Tsinghua University and Baidu, IEEE Access, 2018",
               {"link": url("hotspot")})],
             "Establishes the combinatorial scale of the problem, since a cuboid of n elements has "
             "2 to the power n minus 1 candidate subsets, and reports localisation time falling "
             "from over an hour of manual work to under twenty seconds in production."],
            ["Causal",
             "Difference-in-differences with a placebo test on a pre-treatment window",
             "Attribution is not effect. The control group's own pre-to-post ratio supplies the "
             "counterfactual, and running the same estimator on a window where treatment had not "
             "happened yet tests parallel trends rather than assuming it."],
            ["Feedback",
             [("GLAD: GLocalized Anomaly Detection via Human-in-the-Loop Learning. Islam, "
               "Das, Doppa and Natarajan, 2018", {"link": url("glad")})],
             "Analyst labels tune the weights of an ensemble of simple, explainable detectors "
             "rather than replacing them, on a small explicit label budget. This is the design our "
             "one-click feedback implements."],
            ["Narrate",
             [("Vectara HHEM faithfulness leaderboard, updated May 2026",
               {"link": url("vectara")})],
             "Establishes both that grounded hallucination never reaches zero, hence an "
             "independent numeric verifier, and that small models are competitive on faithfulness "
             "with frontier ones."],
        ],
        widths=[11, 31, 58], size=8.9, pad=4.6, first_bold=True)

    page_break(doc)
    section_heading(
        doc, "Appendix B", "References",
        "Every external claim in this document, with a link. Nothing in this list is our "
        "measurement, and the note column carries the caveat that travels with the figure.")

    order = ["dbt26", "omdia_soc", "spglobal", "gartner_agentic", "vectara", "bird",
             "spider2", "numreason", "psqueeze", "adtributor", "hotspot", "fdr", "glad",
             "rbi_local", "eu_ai_act", "fdic", "zylo"]
    rows = []
    for key in order:
        s = SOURCES[key]
        rows.append([
            [(s["org"], {"bold": True})],
            [(s["title"], {"link": s["url"]}), ("\n" + s["date"], {"colour": T.N500})],
            [(s["note"], None)],
        ])
    table(doc, ["Publisher", "Title and date, linked", "What it is, and its limits"], rows,
          widths=[20, 38, 42], size=8.6, pad=4.4, zebra=True,
          note="Titles are clickable. Where a figure reached us through reporting rather than the "
               "original report, the note says so and the claim is treated as directional.")

    panel(doc, "Claims we could not verify, and what we did about them",
          "An earlier draft of this proposal cited a 91% versus 23% split on banking AI adoption, "
          "and an enterprise text-to-SQL accuracy of roughly 21% against 91% on academic "
          "benchmarks. We could not stand either up against a primary source at the time of "
          "writing, so both have been removed rather than softened. The market-readiness filter in "
          "section 12.1 now stands as our own assumption. The Klarna reversal in section 10.1 is "
          "reported rather than sourced to the company, and is framed as a pattern.",
          accent=T.N400, fill=T.N50, title_colour=T.N600)

    section_heading(doc, "Appendix C", "Glossary")
    table(
        doc,
        ["Term", "What it means in this product"],
        [
            ["KPI contract", "The declared meaning, source fundamentals, grain, quality rules, "
                             "dimensions, ownership, levers and visibility for one metric. One "
                             "YAML file per metric."],
            ["Trust Gate", "The stage that decides whether a figure may be used at all, issuing "
                           "one of five verdicts: PASS, QUARANTINE, WIDE BAND, ABSTAIN or "
                           "WITHHOLD."],
            ["Signal Store", "The durable evidence store on Gold holding investigations, trust "
                             "findings, anomalies, forecasts, causes, recommendations and run "
                             "telemetry."],
            ["Evidence bundle", "The typed set of verified figures and provenance the narrator "
                                "receives. It never contains raw events, and a withheld figure is "
                                "structurally absent from it."],
            ["Engine tag", "The label attached to a figure at the moment it is computed: sql, "
                           "stats, rules, ml or llm. The LLM versus non-LLM breakdown is a query "
                           "over these."],
            ["Persona", "A role-shaped view over one verified claim set. It changes emphasis, "
                        "depth and entitlement, never the underlying number."],
            ["Investigation", "One tenant, one KPI and one pinned time window processed through "
                              "the chain."],
            ["Lever ontology", "The fixed, contract-declared list of actions Decide may propose. "
                               "Nothing outside the list can be recommended."],
            ["Causal rung", "How strong a claim the evidence supports: association, attribution, "
                            "corroborated cause, or estimated effect. Declared, not inferred."],
            ["Observe", "Cross-stage telemetry recording latency, tokens, cost and verifier status "
                        "per stage, which is what makes run cost a measured quantity."],
            ["Modelled figure", "A derived or simulated value that carries its qualifier every "
                                "time it is stated, in every persona."],
        ],
        widths=[20, 80], size=9.1, first_bold=True)
