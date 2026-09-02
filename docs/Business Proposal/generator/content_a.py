"""Front matter, the executive brief, the problem, and the solution design."""
from __future__ import annotations

import theme as T
from sources import url
from docx_kit import (add_run, borders, bullets, code_block, figure, h2, h3, label, panel,
                      para, page_break, rich, section_heading, source_line, stat_band, table)

FIG = "figs/"


# ═════════════════════════════════════════════════════════════════════════════
def front_matter(doc):
    label(doc, "Document control")
    para(doc, "", size=1, space_after=0)
    table(
        doc,
        ["Field", "Detail"],
        [
            ["Prepared for", "Finance, operations, risk and data leadership at a mid-size retail "
                             "bank"],
            ["Submitted by", "Team Nexus, Indian Institute of Technology Patna"],
            ["Problem statement", "BusinessIntelligence.ai, Accenture Innovation Challenge 2026, "
                                  "Round 2"],
            ["Reference build", "FinInsights running end to end on NexaBank, our own banking "
                                "application and event source"],
            ["Date", "September 2026"],
            ["How to read the numbers",
             [("Every figure carries one of four labels. ", None),
              ("Sourced", {"bold": True}),
              (" means an external reference, linked. ", None),
              ("Modelled", {"bold": True}),
              (" means our assumption, stated so you can replace it. ", None),
              ("Illustrative", {"bold": True}),
              (" means a worked example of a method, not output from a run. ", None),
              ("From the build", {"bold": True}),
              (" means it describes what the code does. Nothing here is measured at a client, and "
               "nothing is presented as though it were.", None)]],
        ],
        widths=[24, 76], first_bold=True, size=9.4,
    )

    label(doc, "Contents")
    rows = [
        ["", "Executive brief", "The decision, the numbers, and the ask"],
        ["1", "The problem", "The cost is the day after the alert"],
        ["2", "Solution design", "Seven stages compute. One writes."],
        ["3", "The KPI chain and its contracts", "Five metrics, two cadences, one causal spine"],
        ["4", "Readers and entitlement", "Three people, one set of verified claims"],
        ["5", "Prototype evidence", "The four scenarios the brief asks for"],
        ["6", "Evidence and run cost", "What travels with every insight"],
        ["7", "The feedback loop", "Learning without retraining anything"],
        ["8", "Business case", "A floor we will defend line by line"],
        ["9", "Roadmap", "Three phases, each gated on evidence"],
        ["10", "Risk register", "The three that would kill it are not technical"],
        ["11", "Success criteria", "What to test during a pilot"],
        ["12", "Commercial model", "Where to land, and what it is worth"],
        ["13", "Recommendation", "The decision requested"],
        ["A", "Method register", "The published work behind each tool"],
        ["B", "References", "Every external claim, with a link"],
        ["C", "Glossary", "Terms as this product uses them"],
    ]
    table(doc, ["", "Section", "What it settles"], rows, widths=[6, 34, 60],
          size=9.0, first_bold=True, pad=3.6)


# ═════════════════════════════════════════════════════════════════════════════
def executive_brief(doc):
    page_break(doc)
    section_heading(
        doc, "Executive brief",
        "Your dashboards are fine.\nThe day after the alert is not.",
        first=True)

    para(doc,
         "Every bank in your peer group owns a warehouse, a BI tool and an alerting surface. None "
         "of them answers the question a leader actually asks, which is not what changed but why, "
         "how sure are you, and what should I do about it. Today an analyst answers that by hand, "
         "over most of a working day. FinInsights does that day's work with deterministic tools, "
         "and stays quiet when the evidence will not carry an answer.")

    para(doc,
         "The engine watches five connected banking metrics across two sources that refresh at "
         "different speeds. It checks the data before it says anything about it. It finds the "
         "segment carrying a movement, forecasts with an honest interval, estimates a causal "
         "effect only where the assumptions survive a test, and proposes one action from a closed "
         "list of levers with a named owner. A small language model reads the question and writes "
         "the answer. It never produces a number.")

    panel(doc, "The one decision everything else follows from",
          [("The model may choose the path. It may not choose the numbers. ", {"bold": True}),
           ("Every figure a reader sees is computed by a deterministic tool, written to a store "
            "alongside the engine that produced it, and checked back against that row before the "
            "sentence ships. Switch the model off and not one number changes. The findings still "
            "arrive, in a fixed format instead of prose.", None)])

    h3(doc, "Why this is worth doing now")
    rich(doc, [
        ("Data teams have already adopted AI, but only on one side of the work. In dbt Labs' 2026 "
         "survey of 363 practitioners, 72% now use AI to help write the code that produces their "
         "numbers. Just 24% use it to test, observe or check what comes out. In the same survey, "
         "71% named incorrect or hallucinated output reaching stakeholders as a top concern (",
         None),
        ("dbt Labs, April 2026", {"link": url("dbt26"), "colour": T.BRAND}),
        (").", None),
    ])
    para(doc,
         "The appetite is there. So is the anxiety. What is missing is a layer that treats the "
         "model as a writer rather than a calculator, and that leaves an audit trail a model risk "
         "function will actually accept.")

    label(doc, "What we are claiming, and how sure we are")
    stat_band(doc, [
        ("$335K", "Annual value floor we will defend line by line, before the wider range",
         "Modelled, section 8.1"),
        ("3 to 5", "Months to payback on a bounded implementation and licence profile",
         "Modelled, section 8.2"),
        ("5", "Connected KPIs running end to end on our own banking application today",
         "From the build, section 3"),
        ("0", "Numbers in a narrative the verifier could not trace back to a stored row",
         "By design, section 6.2"),
    ])

    para(doc,
         "The floor is the number to argue with. It is the bottom-up sum of four mechanisms, each "
         "resting on an assumption you can dispute in section 8. A wider range of $550K to $950K "
         "appears once in-time decision value and analyst retention are counted, but we lead with "
         "the floor on purpose. A range we cannot bound is a weaker position than a smaller one we "
         "can.")

    h3(doc, "What we are asking for")
    para(doc,
         "Authorise a governed pilot on the lending and onboarding loop, where KYC completion, "
         "loan approval volume and revenue form one connected story. Use it to replace the "
         "modelled lines in section 8 with measured ones. The Phase 1 exit test is concrete, and "
         "you can run it yourself. The Trust Gate has to quarantine a corrupt batch we seed. The "
         "verifier has to pass on every published figure. An analyst has to be able to review a "
         "completed investigation inside an hour.")


# ═════════════════════════════════════════════════════════════════════════════
def problem(doc):
    section_heading(
        doc, "Section 1", "The cost is not measurement.\nIt is the day after the alert.",
        "Four published figures frame the gap. None of them are ours. They describe the same "
        "failure from four directions: trust, verification, precision, and what happens to "
        "programmes that ignore all three.")

    stat_band(doc, [
        ("71%", "Of data professionals worry about incorrect or hallucinated output reaching "
                "stakeholders", ("dbt Labs, 2026", url("dbt26"))),
        ("24%", "Use AI to test and observe their pipelines, against 72% who use it to write code",
         ("dbt Labs, 2026", url("dbt26"))),
        ("46%", "Of security alerts prove to be false positives, the closest well-measured "
                "analogue", ("Microsoft and Omdia, 2026", url("omdia_soc"))),
        ("42%", "Of firms abandoned most of their AI initiatives during 2025, up from 17%",
         ("S&P Global, 2025", url("spglobal"))),
    ])

    para(doc,
         "Read together they describe one workflow rather than four complaints. Teams are "
         "generating faster than they are checking. People do not trust what comes out. The "
         "alerting surface meant to help is wrong about half the time, so they stop reading it. "
         "Programmes built on top of all three tend not to survive their second year.")

    h2(doc, "Six hours to answer one question, and five and a half of them are clerical", "1.1")
    para(doc,
         "A single metric investigation at a mid-size retail bank takes roughly six analyst hours. "
         "How those hours split is the whole argument.")
    figure(doc, FIG + "01_analyst_day.png",
           "Verification and segmentation are mechanical and repeatable. Judgement, the part only "
           "a person can supply, gets what is left over.")
    para(doc,
         "The ratio is upside down. The last 8% of the effort produces the only artefact a "
         "decision-maker ever reads. The first 92% is reconstruction, and reconstruction is "
         "exactly what a deterministic system does faster, more consistently, and with a trail "
         "that still holds up six months later. At $55 a loaded analyst hour and about 600 "
         "investigations a year, that reconstruction costs roughly $165K.")

    h2(doc, "Three ways the status quo leaks money", "1.2")
    table(
        doc,
        ["", "Mechanism", "Annual cost", "What actually happens"],
        [
            ["1", "The analyst-day", [("$165K", {"bold": True}), ("\nanalyst time", None)],
             "Verification, reconciliation and segmentation eat the investigation. Judgement, the "
             "scarce input, gets the remainder."],
            ["2", "The confidently wrong answer",
             [("$120K to $160K", {"bold": True}), ("\navoidable decisions", None)],
             "A duplicated batch produces a spike that looks statistically real. Charts render it, "
             "alerts fire, a meeting happens. The movement never did. The decision did."],
            ["3", "The reporting bottleneck",
             [("$25K to $40K", {"bold": True}), ("\nduplicated reporting", None)],
             "Finance, operations and analytics need one truth told three ways, with different "
             "figures visible to each. Today that gets built by hand, three times, from one "
             "spreadsheet."],
        ],
        widths=[5, 25, 18, 52], size=9.3,
        note="Modelled from the volumes and unit costs in section 8.4. The cost of analyst time is "
             "externally anchored. The frequencies are ours.")

    h2(doc, "Why the stack you already own cannot close it", "1.3")
    para(doc,
         "Most institutions in this segment own at least three of the four categories below. In "
         "every case the reason the gap survives is structural rather than a missing feature.")
    table(
        doc,
        ["Category", "What it does well", "Why the gap survives"],
        [
            ["BI dashboards", "Render what changed, quickly.",
             "They hold no opinion on whether the change can be trusted, so the burden of proof "
             "lands on an analyst every single time. A dashboard cannot refuse to draw a corrupted "
             "series."],
            ["Alerting", "Tell you something moved.",
             "At roughly half precision the organisational response is to stop reading them. "
             "Volume without precision is noise with a budget line."],
            ["Conversational analytics", "Answer in fluent prose.",
             "Fluency is not accuracy. Leading text-to-SQL systems still miss about one BIRD "
             "question in five, and real warehouse schemas run past a thousand columns where "
             "correct answers run past a hundred lines of SQL."],
            ["Data observability", "Catch the broken pipeline.",
             "Then stop. No segment, no cause, no action, no reader. It tells engineering a table "
             "is stale. It never tells an operations manager which cohort to call."],
        ],
        widths=[19, 22, 59], size=9.3)
    source_line(doc, [
        ("Microsoft and Omdia, State of the SOC 2026", url("omdia_soc")),
        ("BIRD leaderboard", url("bird")),
        ("Spider 2.0, ICLR 2025", url("spider2")),
    ])
    para(doc,
         "These four are complements, not competitors. FinInsights consumes what they produce, "
         "including freshness signals, pipeline health and the warehouse itself. It occupies the "
         "one layer none of them does: a verdict on whether a movement may be spoken about at "
         "all, and to whom.")


# ═════════════════════════════════════════════════════════════════════════════
def solution(doc):
    section_heading(
        doc, "Section 2", "Seven stages compute. One writes.",
        "The architecture is a chain. The Trust Gate sits second on purpose, because its job is to "
        "be able to stop the chain and emit nothing.")

    para(doc,
         "The brief asks teams to show where they use deterministic logic, SQL, business rules, "
         "statistics, traditional ML, causal inference, retrieval and language models, and why. "
         "For this product that answer fits in one picture, so it is worth drawing before anything "
         "else.")

    figure(doc, FIG + "02_engine_boundary.png",
           "Seven of the eight stages run on CPU with no model anywhere in the path. The eighth "
           "turns finished, verified findings into a sentence. This breakdown is read back from "
           "stored records rather than asserted, because every figure carries the engine tag of "
           "the tool that produced it.")

    para(doc,
         "The boundary sits here for a practical reason rather than a cautious one. The two sides "
         "fail differently. A deterministic stage that is wrong is wrong the same way every time, "
         "so you can find it and fix it. A model that is wrong is wrong differently on every run, "
         "in the same confident prose it uses when it is right.")

    h2(doc, "What each stage decides", "2.1")
    table(
        doc,
        ["", "Stage", "Method", "The decision it makes"],
        [
            ["01", "Contract", "Declarative YAML, one file per KPI",
             "What the number means, at what grain, from which fundamentals, and who may see it"],
            ["02", "Trust Gate", "Business rules and SQL invariants",
             "Whether this figure may be used at all, and if not, what gets emitted instead"],
            ["03", "Detect", "Median and MAD residuals, Benjamini-Hochberg FDR control",
             "Whether the move is unlikely, material and persistent enough to interrupt a person"],
            ["04", "Localize", "PSqueeze over the segment cube, LMDI-I decomposition",
             "Which cells carry the movement, how much each explains, and how much is left over"],
            ["05", "Forecast", "Method registry scored on rolling-origin MASE",
             "What to expect next, as an interval, and how wide that interval honestly has to be"],
            ["06", "Causal", "Difference-in-differences with a placebo test",
             "How much of the movement an intervention actually caused, or that we cannot say"],
            ["07", "Decide", "Rules over a closed lever library in YAML",
             "Which approved lever to propose, to which owner, at what expected impact range"],
            ["08", "Narrate", "Small local model, then a numeric verifier",
             "How the finding reads for this reader at this entitlement tier, and nothing more"],
        ],
        widths=[5, 15, 30, 50], size=9.1, pad=4.6,
        note="Observe runs across all eight rather than after them. Section 6.3 shows what it "
             "records.")

    h2(doc, "Reference architecture", "2.2")
    para(doc,
         "The platform is a set of bounded services rather than one analytics application. The "
         "warehouse terminates in ClickHouse across three layers. The intelligence stages read "
         "through a Metric API and write findings to a Signal Store. Delivery is a dashboard plus "
         "a human approval step that no action can go around.")
    figure(doc, FIG + "04_architecture.png",
           "Two properties carry most of the governance weight. The intelligence stages never "
           "query raw events; they ask the Metric API for declared, additive fundamentals at an "
           "explicit grain, which stops a free-form answer engine turning into an ungoverned SQL "
           "layer. And the Signal Store sits between the tools and the narrator, so the narrator "
           "physically cannot see anything that has not already been computed, verified and "
           "recorded.")

    para(doc,
         "The three warehouse layers are conventional, deliberately so. Bronze holds raw events "
         "exactly as received and is never edited, which is what makes it the audit trail. Silver "
         "is cleaned: names canonicalised, duplicates removed by event identity, personal data "
         "masked, sessions rebuilt, one agreed day and timezone. Gold holds the serving rollups, "
         "the segment cube and the Signal Store. The dashboard and the tools read Silver and Gold. "
         "Neither ever reads Bronze.")

    h2(doc, "The Trust Gate has five answers, not two", "2.3")
    para(doc,
         "This is the component the rest of the proposal rests on. Most analytics systems have two "
         "states: answer, or error. This one has five. Each produces a different artefact for the "
         "business and a different one for engineering, so a refusal has somewhere to go instead "
         "of being a dead end.")
    table(
        doc,
        ["Input condition", "Verdict", "Emitted to the business", "Emitted to engineering"],
        [
            ["A hard invariant fails", [("QUARANTINE", {"colour": T.FALL, "bold": True})],
             "Nothing. The metric is withheld and the movement is never narrated.",
             "Incident note naming the failing check"],
            ["The movement is real and material",
             [("PASS", {"colour": T.RISE, "bold": True})],
             "The full finding: trust, driver, trajectory, cause, action, owner.", "Nothing"],
            ["History is too short to trust", [("WIDE BAND", {"colour": T.WARN, "bold": True})],
             "Movement and localisation only. The forecast comes back as an explicit wide band.",
             "Coverage note"],
            ["A defect and a real event both fit",
             [("ABSTAIN", {"colour": T.WARN, "bold": True})],
             "Ranked hypotheses, what is missing, and the single cheapest check that settles it.",
             "Data request"],
            ["The reader is not entitled", [("WITHHOLD", {"colour": T.N600, "bold": True})],
             "The figure is structurally absent from the bundle, and so is anything it could be "
             "back-computed from.", "Access-decision log"],
        ],
        widths=[24, 14, 38, 24], size=9.0, pad=4.6)

    panel(doc, "Why five and not two",
          "A binary gate pushes every ambiguous case into one of two wrong answers: publish a "
          "number that might be an artefact, or bury a movement that might be real. The middle "
          "three verdicts exist because those are the cases that actually turn up. WIDE BAND keeps "
          "a genuine movement visible while refusing to pretend the forecast is tight. ABSTAIN "
          "turns a stalemate into a work item by naming the cheapest check. WITHHOLD removes a "
          "figure structurally rather than redacting it afterwards, which is the difference "
          "between an entitlement control and a display rule.")

    h2(doc, "Four properties the commercial claims rest on", "2.4")
    table(
        doc,
        ["Property", "What it means in the build", "The claim it makes defensible"],
        [
            ["Determinism", "Every figure is computed on CPU with no training data. The same "
                            "frozen rows produce byte-identical numeric output.",
             "A figure can be reproduced in an audit six months later without an engineer"],
            ["Optional narrative", "Turning the narrator off changes no number. Findings fall back "
                                   "to a bounded template and the verifier still runs.",
             "The bank is never operationally dependent on a model provider"],
            ["Declared contracts", "One YAML per metric: formula, grain, materiality threshold, "
                                   "freshness SLA, entitlement scope, permitted dimensions, "
                                   "owners, levers.",
             "Onboarding a second institution is configuration, not a rebuild"],
            ["In-tenant residency", "The Signal Store and the narrator both run inside the tenant. "
                                    "Raw events never enter model context.",
             "Payment data never leaves the jurisdiction, and the prompt-injection surface stays "
             "closed"],
        ],
        widths=[17, 44, 39], size=9.1, first_bold=True)

    rich(doc, [
        ("Residency is not a preference here. Since April 2018 the Reserve Bank of India has "
         "required payment system operators to store the full end-to-end details of payment "
         "transactions on systems located only in India, with compliance evidenced by a "
         "board-approved audit from a CERT-In empanelled auditor (", None),
        ("RBI circular RBI/2017-18/153", {"link": url("rbi_local"), "colour": T.BRAND}),
        ("). A design that posts raw banking data to an external model endpoint does not clear "
         "that review. Ours never sends one.", None),
    ])
