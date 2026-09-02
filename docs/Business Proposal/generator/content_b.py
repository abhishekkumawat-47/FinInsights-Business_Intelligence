"""Sections 3 to 7: the KPI chain, the readers, the prototype evidence, telemetry, feedback."""
from __future__ import annotations

import theme as T
from sources import url
from docx_kit import (add_run, bullets, code_block, figure, h2, h3, label, panel, para,
                      page_break, rich, section_heading, source_line, stat_band, table)

FIG = "figs/"


# ═════════════════════════════════════════════════════════════════════════════
def kpis(doc):
    section_heading(
        doc, "Section 3", "Five metrics, two cadences,\none causal spine",
        "We build one connected chain rather than twenty independent metrics, because a chain "
        "answers questions a collection cannot. Why did revenue drop is answered by walking it.")

    para(doc,
         "Five is a deliberate number. It is enough for a movement in one metric to explain a "
         "movement in another, and few enough that each one can carry a real contract, real "
         "quality rules and a named owner instead of a placeholder.")

    figure(doc, FIG + "03_kpi_chain.png",
           "Fewer signups or weaker KYC completion lead to fewer approvals, which lead to lower "
           "revenue. A failure spike can drag any of them down. Because the contracts declare "
           "these edges, several metrics moving at once become one story with a driver chain "
           "instead of four alerts a human has to recognise as the same incident.")

    h2(doc, "The method follows the shape of the metric", "3.1")
    rich(doc, [
        ("This is a bank, not a shop, so we do not use a retail price, volume and mix "
         "decomposition. The reason is arithmetic rather than taste. Adtributor's authors made the "
         "same distinction in 2014: a derived measure such as a ratio cannot be attributed the way "
         "an additive measure can, because a single element can show zero surprise and still "
         "account for more than 100% of the change (", None),
        ("Bhagwan et al., USENIX NSDI 2014", {"link": url("adtributor"), "colour": T.BRAND}),
        (").", None),
    ])
    table(
        doc,
        ["Shape", "KPIs", "How a movement gets explained"],
        [
            ["Rate through a funnel", "KYC completion, transaction failure",
             "Always on the two underlying counts, never on the ratio. Which stage leaked, and "
             "which segment drove the leak."],
            ["Count", "Signups, loan approval volume",
             "Segment and time, over the additive cube. Contributions sum, so the residual means "
             "something."],
            ["Money", "Revenue",
             "Which fee line moved, then which upstream volume driver in the chain moved it."],
        ],
        widths=[22, 26, 52], size=9.3, first_bold=True)

    h2(doc, "Two sources, two cadences, one rule about which one counts", "3.2")
    table(
        doc,
        ["Source", "Grain and cadence", "Role", "SLA"],
        [
            ["Daily banking snapshot",
             "Application, account and transaction grain, extracted once a day from NexaBank's "
             "Postgres",
             [("Produces every KPI value.", {"bold": True}),
              (" All five numbers come from here.", None)],
             "120 min"],
            ["Real-time clickstream", "Per event, streamed through Kafka",
             [("Behavioural context only.", {"bold": True}),
              (" Funnel-stage detail and journey reconstruction. Never a figure a reader sees as "
               "a KPI.", None)],
             "15 min"],
        ],
        widths=[20, 31, 37, 12], aligns=["l", "l", "l", "r"], size=9.1, first_bold=True,
        note="The two cadences are the point, not an inconvenience. Each source carries its own "
             "SLA, and a KPI combining a real-time number with a daily one is computed against the "
             "oldest common data time. Too large a gap is itself a finding.")

    para(doc,
         "The discipline behind that split matters more than it reads. The clickstream sees a "
         "customer begin identity verification in the interface, but it covers only the sampled "
         "population and its dimensions are synthesised per session. Use it as a denominator and "
         "you get a confident, wrong completion rate. The contract says so in writing, so an "
         "analyst challenging the figure can see which source produced it without asking anyone.")

    h2(doc, "The contract is the semantic layer and the portability layer at once", "3.3")
    para(doc,
         "One YAML file per metric declares everything the engine is allowed to assume. The "
         "narrator uses these definitions and nothing else, which makes metric meaning "
         "configuration rather than code.")
    code_block(doc, [
        ("id: kyc_completion_rate", "#C4B5FD"),
        ("formula: kyc_completed / kyc_started        # the RATE is not additive.", "#F5F3FB"),
        ("additivity: non-additive                    # its two counts are.", "#8D86A1"),
        ("aliases: [kyc, identity verification, onboarding completion]", "#F5F3FB"),
        ("grain: {time: daily, entity: application}", "#F5F3FB"),
        ("", "#F5F3FB"),
        ("sources:", "#C4B5FD"),
        ("  - id: nexabank_core        # the value comes from core banking", "#F5F3FB"),
        ("    cadence: hourly_batch", "#F5F3FB"),
        ("    freshness_sla_minutes: 120", "#F5F3FB"),
        ("  - id: nexabank_clickstream", "#F5F3FB"),
        ("    role: corroboration      # counts UI starts, not submissions", "#8D86A1"),
        ("", "#F5F3FB"),
        ("detect:   {fdr: benjamini_hochberg, persistence_windows: 3}", "#C4B5FD"),
        ("localize: {dimensions: [channel, region, device, kyc_step]}", "#C4B5FD"),
        ("levers:   [fix_kyc_step, review_document_rules, escalate_vendor]", "#C4B5FD"),
        ("visibility: {cfo: full, ops_manager: full, analyst: method}", "#C4B5FD"),
    ], caption="An abridged contract, from the build. It declares the definition, the grain, the "
               "additive fundamentals, which dimensions may be localised, the reliability checks, "
               "the access rules and the closed list of actions Decide may recommend. Contracts "
               "name physical columns and are validated against the live schema rather than "
               "trusted, because a contract naming a key that does not exist reads empty rather "
               "than failing loudly.")

    para(doc,
         "The commercial consequence is direct. Onboarding a new institution means mapping its "
         "event vocabulary and writing its contracts. It does not mean rewriting the reasoning "
         "stages. One is a product. The other is a consulting engagement.")


# ═════════════════════════════════════════════════════════════════════════════
def personas(doc):
    section_heading(
        doc, "Section 4", "Three readers, one set of verified claims",
        "A persona changes emphasis, depth and entitlement. It never changes the underlying "
        "number.")

    table(
        doc,
        ["Reader", "Today", "With FinInsights", "Cadence"],
        [
            ["CFO", "Waits for a weekly pack. Follow-ups take days.",
             "Position and outlook on demand, with revenue at risk attached to the driver that "
             "explains it", "Weekly and ad hoc"],
            ["Operations Manager", "Knows a metric fell. Guesses the segment.",
             "A named segment, a named lever, a named owner, and impact as a range, with revenue "
             "structurally absent", "Daily"],
            ["Analyst", "Spends the day verifying and segmenting.",
             "Reviews and challenges a completed investigation, including the method and the "
             "residual", "Daily"],
        ],
        widths=[16, 26, 44, 14], size=9.2, first_bold=True,
        note="Risk and audit read the same evidence bundle without a persona of their own in the "
             "prototype. A dedicated reader is Phase 2 configuration, not engineering.")

    h2(doc, "Entitlement is enforced, not displayed", "4.1")
    para(doc,
         "Personas resolve server-side, so a request can never widen access. The Metric API "
         "applies the row-level entitlement clause declared in the contract, and it does so before "
         "any claim is assembled. A restricted figure is never phrased and then redacted. It is "
         "never built.")
    para(doc,
         "The check most implementations miss is the second-order one. If a restricted numerator "
         "could be back-computed from a published ratio, that ratio is suppressed too. Section 5.4 "
         "shows it running.")

    h2(doc, "The decision workflow, end to end", "4.2")
    bullets(doc, [
        ("Signal.  ", "A scheduled sweep or a user question pins a KPI, a time window and an "
                      "ingest watermark."),
        ("Evidence.  ", "The Metric API reads declared fundamentals. The Trust Gate checks "
                        "readiness, quality, reconciliation and freshness, then issues one of five "
                        "verdicts."),
        ("Explanation.  ", "Detect, Localize, Forecast and Causal build the finding to the depth "
                           "the contract permits and no further. The causal ceiling is declared, "
                           "not discovered."),
        ("Action.  ", "Decide proposes a contract-approved lever and names the accountable owner, "
                      "with expected impact as a range."),
        ("Review.  ", "The reader sees the verified narrative and the evidence trail. A human "
                      "approves any action, and the outcome is written back against the finding "
                      "that proposed it."),
    ])


# ═════════════════════════════════════════════════════════════════════════════
def evidence_scenarios(doc):
    section_heading(
        doc, "Section 5", "The four scenarios, on one seeded dataset",
        "The brief asks for four specific behaviours. Each one below runs on a single seeded "
        "NexaBank dataset, and every anomaly exists in the source data before the engine sees it.")

    panel(doc, "Two rules that keep this section honest",
          [("First, an anomaly has to exist in the source data before the engine sees it. ",
            {"bold": True}),
           ("When a scenario says loan demand spikes, NexaBank generates the extra loan events, "
            "and the simulator writes its own ground truth to a fixture file. The gate script "
            "then scores the Signal Store against that fixture rather than against our "
            "expectations." + chr(10), None),
           ("Second, the four charts below are worked examples, not production output. ",
            {"bold": True}),
           ("They are tagged illustrative on the chart itself. This prototype has run on seeded "
            "data, not at a client and not at production volume. Presenting a modelled series as "
            "a measured one is the exact failure this product exists to prevent, so we do not do "
            "it in our own proposal either.", None)])

    para(doc,
         "Every scenario starts the same way, with a decision about whether there is anything to "
         "discuss at all. Detect scores the day against the stored forecast band using median and "
         "median-absolute-deviation residuals, so a fresh anomaly cannot quietly contaminate its "
         "own baseline. It fires only when a move is unlikely, material and persistent across "
         "several windows.")
    figure(doc, FIG + "05_detect_band.png",
           "Detection on loan approval volume. The persistence window and the false-discovery "
           "alpha are both declared in the KPI contract, so what counts as material is a business "
           "decision rather than an engineering default.")
    rich(doc, [
        ("Across many series, volume alone manufactures alarms, so p-values are corrected with "
         "Benjamini-Hochberg false discovery control. That is not a tuned threshold. It is a "
         "published method that gives a guaranteed lower bound on precision without any labelled "
         "data (", None),
        ("Rebjock et al., NeurIPS 2021", {"link": url("fdr"), "colour": T.BRAND}),
        (").", None),
    ], size=9.6, colour=T.N600)

    h2(doc, "A multi-factor movement, with the residual published", "5.1")
    para(doc,
         "Revenue drops. The engine walks the chain instead of modelling revenue directly, and "
         "reports one story with ranked contributions rather than four simultaneous alerts.")
    figure(doc, FIG + "06_waterfall.png",
           "Contribution decomposition, drawn as a waterfall. Contributions are computed on "
           "additive counts only, and the unexplained residual is published rather than absorbed "
           "into the largest driver.")
    rich(doc, [
        ("Publishing the residual is not modesty. PSqueeze is the first localisation method to "
         "detect root causes lying outside the recorded cube, reporting 0.90 F1 on that task, and "
         "the paper is explicit that earlier approaches returned a confident but wrong attribution "
         "in the same situation (", None),
        ("Li et al., Journal of Systems and Software, 2023", {"link": url("psqueeze"),
                                                              "colour": T.BRAND}),
        ("). A method that can be wrong quietly is worse than one that says so.", None),
    ])

    h2(doc, "Low confidence, and a refusal that names its own next step", "5.2")
    para(doc,
         "A spike arrives that the Trust Gate suspects is a duplicated batch, while the calendar "
         "shows a marketing campaign in the same window. The evidence genuinely conflicts, so the "
         "engine abstains.")
    panel(doc, "What the reader actually receives",
          [("A 41% rise in signups was detected between 12 and 18 August and is not being reported "
            "as a business movement. Two explanations fit the evidence: a duplicated ingest batch, "
            "and the tier-2 campaign that launched on 12 August. The cheapest check that separates "
            "them is a distinct count of source event identities for 12 to 14 August against the "
            "batch manifest. Until that check returns, no figure from this window is published.",
            {"italic": True})],
          accent=T.WARN, fill="#FDF6EC", title_colour=T.WARN)
    rich(doc, [
        ("Abstention is not silence. It names the ranked hypotheses, what is missing, and the one "
         "check that would settle it, which turns a stalemate into a work item with an owner. It "
         "is also worth designing rather than hoping for: on Vectara's leaderboard, model answer "
         "rates range from 100% down to 67%, so willingness to decline varies enormously between "
         "models and cannot be left to the model's discretion (", None),
        ("Vectara HHEM leaderboard", {"link": url("vectara"), "colour": T.BRAND}),
        (").", None),
    ])

    h2(doc, "A new product with nine days of history", "5.3")
    figure(doc, FIG + "07_sparse_fan.png",
           "A sparse series returns a wide, explicitly caveated range and the number of days "
           "available. Detect does not fire. Localize abstains per dimension below a minimum cell "
           "count. Thin history is a first-class output here, not a degraded one.")
    para(doc,
         "The method changes with data volume. The honesty does not. The forecast registry will "
         "only use a method that beats the contract's own baseline on rolling-origin MASE for that "
         "series, so a model never gets chosen simply because it is available.")

    h2(doc, "The same insight, two readers, one claim set", "5.4")
    table(
        doc,
        ["", "CFO", "Operations Manager"],
        [
            ["Movement", "KYC completion fell 6.2 points week on week",
             "KYC completion fell 6.2 points week on week"],
            ["Driver", "Mobile, tier-2 cities, document upload step. 71% of the drop.",
             "Mobile, tier-2 cities, document upload step. 71% of the drop."],
            ["Revenue at risk", [("$84K over the quarter", {"colour": T.BRAND_DEEP,
                                                            "bold": True})],
             [("Absent from the bundle. Not redacted. Never assembled.",
               {"colour": T.N500, "italic": True})]],
            ["Approval-rate ratio", "Shown",
             [("Suppressed, because revenue at risk can be back-computed from it",
               {"colour": T.N500, "italic": True})]],
            ["Action", "Noted, with the owning function named",
             "Escalate to the identity vendor. Owner: onboarding operations. Expected recovery 20% "
             "to 80% of the gap."],
        ],
        widths=[18, 41, 41], size=9.1, first_bold=True,
        note="Illustrative, using the entitlement rules the contracts declare.")

    h2(doc, "Coverage against the brief's minimum expectations", "5.5")
    table(
        doc,
        ["The brief asks for", "Where this proposal satisfies it"],
        [
            ["Three to five connected KPIs across two or three sources with different cadences",
             "Five-KPI chain over two sources at daily and per-event cadence, section 3"],
            ["A lightweight KPI or semantic contract",
             "One YAML per metric: definition, calculation, drivers, thresholds, lineage, access. "
             "Section 3.3"],
            ["At least two personas with different narratives or actions",
             "Three, resolved server-side, over one claim set. Sections 4 and 5.4"],
            ["One multi-factor movement with known drivers",
             "Revenue drop decomposed across KYC leak, failures and mix. Section 5.1"],
            ["One low-confidence scenario with clarification or abstention",
             "The ABSTAIN verdict, with the cheapest confirming check named. Section 5.2"],
            ["One sparse-history or newly launched KPI",
             "Nine-day product launch returning a wide caveated band. Section 5.3"],
            ["One role-based security or entitlement scenario",
             "Revenue withheld from operations, and the ratio suppressed too. Section 5.4"],
            ["Evidence: freshness, method, contribution, confidence, lineage",
             "The evidence card carried by every insight. Section 6.1"],
            ["A clear breakdown of LLM versus non-LLM processing",
             "Engine tags stored per figure, read back rather than asserted. Sections 2 and 6.2"],
            ["Runtime telemetry: latency, model calls, tokens, estimated cost",
             "Observe, one row per stage per run. Section 6.3"],
        ],
        widths=[42, 58], size=9.1, zebra=True)


# ═════════════════════════════════════════════════════════════════════════════
def telemetry(doc):
    section_heading(
        doc, "Section 6", "What travels with every insight",
        "An insight nobody can interrogate is a rumour with formatting. Three artefacts travel "
        "with every finding, and all three are read from stored records.")

    h2(doc, "The evidence card", "6.1")
    table(
        doc,
        ["Field", "What it holds", "Why a sceptic needs it"],
        [
            ["Freshness", "Data time per source against that source's SLA",
             "Tells a real decline apart from a late batch"],
            ["Method", "Which tool ran, with its parameters",
             "Lets the method be argued with rather than trusted"],
            ["Contribution", "Each driver's share, and the unexplained residual",
             "Shows what the explanation does not cover"],
            ["Confidence", "The interval, and the basis for it",
             "Separates a tight estimate from a wide one"],
            ["Lineage", "Metric id, contract version, query hash, window, source rows",
             "Reproduces the figure without an engineer"],
        ],
        widths=[16, 42, 42], size=9.2, first_bold=True)

    h2(doc, "The engine breakdown is a query, not the model's opinion", "6.2")
    para(doc,
         "Every produced number is tagged at the moment it is computed with the engine that made "
         "it: SQL, statistics, rules, ML or LLM. The breakdown shown on an insight is a query over "
         "those tags. It is a fact about what ran, never a claim the model makes about itself.")
    rich(doc, [
        ("The alternative is unfalsifiable, and worse than it sounds. Ask a model which parts of "
         "its answer were computed rather than generated and you get a fluent, plausible answer "
         "with no relationship to what happened. Grounded hallucination does not reach zero for "
         "any model on Vectara's leaderboard, even when the source text is handed to it, which is "
         "why an independent numeric verifier sits between the narrator and the reader (", None),
        ("Vectara, May 2026", {"link": url("vectara"), "colour": T.BRAND}),
        (").", None),
    ])

    h2(doc, "Run cost is measured, not asserted", "6.3")
    figure(doc, FIG + "08_observe_record.png",
           "Observe writes one row per stage per run. Because engine, latency, tokens, estimated "
           "cost and verifier status are columns rather than estimates, the marginal cost of an "
           "additional governed metric is something the customer watches rather than something we "
           "claim.")
    rich(doc, [
        ("The cost shape is the argument for a small local model. Narration is output-heavy, and "
         "output tokens are the expensive kind on hosted APIs, so a narration-heavy design is the "
         "costly one to outsource. Quality does not obviously argue the other way either: on the "
         "same faithfulness leaderboard, Microsoft's Phi-4 sits at 3.7% and Llama-3.3-70B at 4.1%, "
         "against 3.1% for GPT-5.4-nano (", None),
        ("Vectara, May 2026", {"link": url("vectara"), "colour": T.BRAND}),
        ("). For a stage whose only job is to phrase numbers it has been handed, a small model is "
         "competitive, and it sits behind your firewall.", None),
    ])
    panel(doc, "What we are not claiming",
          "We are not quoting a cost per insight. This prototype has not run at production volume, "
          "so any figure we published would be an estimate dressed as a measurement. Self-hosting "
          "also only beats a managed API above a workload floor, and an idle GPU inflates unit "
          "cost badly. Our case for on-premise serving rests on data residency first and cost "
          "second. If a bank's volume sits below the floor, the deployment is still correct. It is "
          "just not cheaper, and we would say so.",
          accent=T.N400, fill=T.N50, title_colour=T.N600)


# ═════════════════════════════════════════════════════════════════════════════
def feedback(doc):
    section_heading(doc, "Section 7", "Learning without retraining anything")
    para(doc,
         "One click on each insight: was the root cause correct, was this a known event such as a "
         "holiday, was the action taken. The response writes a structured row that does exactly "
         "three things.")
    bullets(doc, [
        "Adds a suppression or known-event rule that Detect reads on its next run.",
        "Adjusts a method-reliability weight used when ranking candidate causes.",
        "Corrects a definition in a KPI contract, with the change versioned.",
    ])
    para(doc,
         "No model is retrained, and no lever list is ever widened by learning. That boundary is "
         "deliberate. A feedback loop that can invent a new recommended action is a feedback loop "
         "that has escaped its governance.")
    rich(doc, [
        ("The design has published support. GLAD shows analyst labels tuning the weights of an "
         "ensemble of simple, explainable detectors rather than replacing them, on a small and "
         "explicitly budgeted number of labels. Its stated premise is that practising analysts "
         "want to keep detectors they can explain (", None),
        ("Islam, Das, Doppa and Natarajan, 2018", {"link": url("glad"), "colour": T.BRAND}),
        (").", None),
    ])
