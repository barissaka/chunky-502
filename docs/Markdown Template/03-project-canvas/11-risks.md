# Risks

Record here the strategic risks identified at the start of the project. Write each risk as an **event** that could happen, not as a general worry: "Recall@5 on the evaluation set stays below 0.60 at the end of Sprint 3", not "the model fails".

## Risks, assumptions and constraints

A risk is an uncertain event that would hurt the project if it happens. It is connected to two other entries in the charter:

- **Every assumption has a risk on its flip side.** Each assumption in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) has an ID (A-01, …) and names its linked risk. Register that risk here, give it an ID (R-01, …), and write the assumption's ID in **Linked to**. The IDs must point both ways. Example: the assumption "the dataset covers the in-scope categories" has the risk "the dataset under-represents some categories, leading to poor performance on them".
- **The uncertain part of a constraint is a risk.** A constraint in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) is a fixed limit, but complying with it can fail. The in-scope activity in [Major Activities](03-project-canvas_v2/04-major-activities.md) that enforces the constraint is the risk's mitigation. Example: the constraint "no PII is stored" has the risk "users submit PII in free-text queries, and it ends up in logs or the retrieval index"; PII masking is the mitigation.

A risk can also come from a dependency in [Dependencies](03-project-canvas_v2/06-dependencies.md), for example an external API that changes or becomes unavailable. Write the dependency's row number in **Linked to**.

## How to fill in each risk

Each risk has three parts that act at different times. Keep them separate.

| Field | When it acts | Question it answers |
|---|---|---|
| **Mitigation** | **Before** the risk happens | How do I lower its probability or impact? |
| **Contingency plan (B plan)** | **After** the risk happens | If it happens anyway, what will I do? |
| **Probability / Impact** | The situation **after** mitigation | Given the mitigation, how likely is it and how bad would it be? |

**Probability is residual probability:** what remains after the mitigation is applied. Do not write "we will try several models, so probability is 1". The mitigation is already counted. If your mitigation really brings the probability down to 1, the item is not a risk.

### Probability (1–5)

| Value | Meaning |
|---|---|
| 1 | Very low (&lt;10%): rare in the literature, no sign in pilot tests |
| 2 | Low (10–30%): possible, but only under special conditions |
| 3 | Medium (30–50%): seen in about half of similar projects |
| 4 | High (50–75%): typical in this area; it would be a surprise if it did not happen |
| 5 | Very high (>75%): almost certain. If it is basically going to happen, treat it as a constraint in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md). If some uncertainty remains, keep it as an assumption in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) and link this risk to it |

Every probability value needs a **basis**, written next to it: a pilot measurement, the literature, a data profile (e.g., the class or category distribution), a third-party dependency, or team experience. "3, because it feels medium" cannot be defended. "3, because the pilot retrieval test gave Recall@5 = 0.52" can.

### Impact (1–5)

Rate impact by the **worst** of the three columns:

| Value | Schedule | Budget (incl. cloud credits) | Target / Scope |
|---|---|---|---|
| 1 | &lt;2 weeks | &lt;2% | Not noticeable |
| 2 | 2–4 weeks | 2–5% | A secondary metric is affected |
| 3 | 1–2 months | 5–10% | A technical requirement is partly unmet |
| 4 | 2–4 months | 10–20% | An acceptance criterion is not met |
| 5 | >4 months | >20% | The output is unacceptable; the objective is not achieved |

**A risk that threatens an acceptance criterion or success criterion has an impact of at least 4.**

### Risk score and what each band requires

**Risk score = Probability × Impact** (1–25).

| Score | Band | Required |
|---|---|---|
| 1–4 | Low | Monitoring is enough |
| 5–9 | Medium | Define a mitigation |
| 10–14 | High | Mitigation **and** trigger **and** contingency plan **and** named owner are all required |
| 15–25 | Critical | Review the project design. Also explain below the table when the risk will be re-evaluated and which early measurement will test it |

A healthy table has a few high risks, mostly medium ones and a few low ones. If every row is 1–2, it reads as "no risk analysis was done". If every row is 4–5, the project looks infeasible.

### Contingency plan: three-question test

Ask these three questions of every contingency plan:

1. **Would I have done this anyway?** If yes, it belongs in the Major Activities, not here. "Try different models", "tune hyperparameters" and "keep testing and optimizing" are not contingency plans.
2. **What is the trigger?** A contingency plan needs a **numeric threshold** and a **date or sprint**. Write "If groundedness on the evaluation set is &lt; 0.70 at the end of Sprint 4, …", not "If performance stays low, …".
3. **Who is the owner?** Name the person who decides to narrow the scope, switch the model or renegotiate the target with the AI customer. "The project team" is not an owner. Every member manages the project in some capacity, so an owner is always a named person, together with the role they hold in [Project Organization](03-project-canvas_v2/08-project-organization.md).

| Not a contingency plan | Contingency plan |
|---|---|
| "Different models will be compared." | "If the target is not met, the system is released only for the categories that meet it; the rest stay manual." |
| "Expert validation will be done." | "If label agreement is κ < 0.70, those classes are excluded from the evaluation and the AI customer is informed in writing." |
| "Hyperparameter optimization will be done." | "If GPU memory is not enough, a 4-bit quantized model is used and the latency target is renegotiated." |

If you are stuck, use one of these four patterns:

- **Narrow the scope:** release on the subset that meets the target and leave the rest manual.
- **Degrade gracefully:** give a narrower output instead of the full one (e.g., retrieved passages and a structured summary instead of a generated answer).
- **Hand over to a human (human-in-the-loop):** below a confidence threshold, the system stops producing output and routes the case to a person.
- **Renegotiate the target:** document what cannot be measured and revise the scope with the AI customer.

## Where risks come from

Do not write only "the model may not work". Write **at least one risk from each of the five layers**. A table with only technical risks is incomplete. The same five layers are used as the constraint categories in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md).

| Layer | Typical risks |
|---|---|
| **Data** | Label noise, class imbalance, delayed data access, distribution shift (data drift, concept drift) |
| **Model** | Target metric not met, collapse on rare classes, uncalibrated confidence scores, bias |
| **Infrastructure** | Not enough GPU or memory, latency target not met, failure to scale, fluctuation or loss of assigned resources |
| **Integration** | An external API changes, authorization or access is delayed |
| **People / process** | No domain expert available for labelling or evaluation, user acceptance not obtained, a team member leaves |

Across the layers, cover the whole life cycle: data preparation, model development, deployment and maintenance. Include model decay after deployment and say what will trigger maintenance.

**Not risks:**

- A fixed limit is a **constraint**. For example, "limited computational resources" belongs under Assumptions & Constraints. The resources fluctuating or failing *is* a risk.
- An **assumption** is logged in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md), not here. Its flip-side risk is registered here, with the assumption's ID in **Linked to**.
- Work the team will not do is an **out-of-scope activity** in [Major Activities](03-project-canvas_v2/04-major-activities.md).

## Risk register

Add rows as needed. Rows with a score of 10 or more also need a detail block (next section).

| # | Layer | Risk (event) | When / where | Probability | Impact | Score | Owner | Linked to |
|---|---|---|---|---|---|---|---|---|
| R-01 | Data | At least one of the four added regulations cannot be extracted with its article boundaries (scanned or unconsolidated text) by M1 | Sprint 1; development | 2 | 3 | 6 | Data Scientist (Özge Çalışkan) | A-01, C-01; Dependencies row 1 |
| R-02 | Data | FAQ pages and forums yield fewer than 30 in-scope questions, or fewer than 5 in a question type, by M2 | Sprint 1; development | 3 | 4 | 12 | Business Analyst (Ekin Deniz Öztürk) | A-02 |
| R-03 | People / process | Fewer than 10 participants complete the default-state session (M2) or the pilot session (M9) | Sprints 1 and 4; development | 3 | 4 | 12 | Product Owner (Zehranur Aymaz Kutluyer) | A-03; Dependencies row 3 |
| R-04 | Infrastructure | The cost of the Law-only baseline run, extrapolated to the two larger corpus sizes, exceeds 50% of the $100 credit, so a larger run is dropped at M4 | Sprint 2; development | 2 | 3 | 6 | Data Scientist (Barış Saka) | C-04, C-08 |
| R-05 | Data | An amendment changes an article used in the answer key between 26/10/2026 and 30/12/2026 | Sprints 1–4; development. After deployment the same event makes answers outdated and triggers maintenance | 3 | 3 | 9 | Business Analyst (Ekin Deniz Öztürk) | A-04, C-02 |
| R-06 | People / process | The terms of use of a chosen forum prohibit collecting or storing its content, and its questions must be dropped | Sprint 1; development | 2 | 2 | 4 | Business Analyst (Ekin Deniz Öztürk) | A-05 |
| R-07 | Model | The assistant answers an out-of-scope question or gives advice on an individual case instead of declining | Sprints 3–4; development and after deployment | 3 | 4 | 12 | Data Scientist (Barış Saka) | C-01, C-05, C-11 |
| R-08 | Infrastructure | Google Cloud credit spend reaches $100 before 30/12/2026 | Sprints 2–4; development | 2 | 4 | 8 | Data Scientist (Özge Çalışkan) | C-06, C-08; Dependencies row 4 |
| R-09 | People / process | A team member cannot work on the project for more than 2 consecutive weeks | Sprints 1–4; development | 2 | 2 | 4 | Product Owner (Zehranur Aymaz Kutluyer) | C-10 |
| R-10 | Data | A user types personal data (name, national ID number, licence plate) into a question and it is written to a log unmasked | Sprints 3–4; development and after deployment | 2 | 3 | 6 | Data Scientist (Özge Çalışkan) | C-12 |
| R-11 | Model | The share of correct answers or of supported article references on the 30 in-scope questions is below 80% at M7 | Sprints 2–3; development | 3 | 4 | 12 | Product Owner (Zehranur Aymaz Kutluyer) | C-04 |
| R-12 | Model | At M5 the RAG pipeline scores no higher than the long-context baseline on correctness and on article citation | Sprint 2; development | 4 | 2 | 8 | Data Scientist (Barış Saka) | C-04 |
| R-13 | Integration | The hosted model API on Google Cloud changes its model version or quota, or is unavailable for more than 1 day, during an evaluation or pilot week | Sprints 2–4; development | 2 | 2 | 4 | Data Scientist (Özge Çalışkan) | C-06; Dependencies row 4 |
| R-14 | Model | At M7 fewer than 4 of the 5 follow-up questions in the question set are answered correctly, because the reference to the earlier turn is resolved to the wrong article | Sprints 2–3; development and after deployment | 3 | 3 | 9 | Data Scientist (Barış Saka) | C-05 |
| R-15 | Model | On the ambiguity labels at M7, the ask decision has precision or recall below 0.70: the assistant asks when no condition is missing, or answers without asking when a missing condition changes the answer | Sprints 2–3; development and after deployment | 3 | 3 | 9 | Data Scientist (Özge Çalışkan) | C-05 |

"When / where" gives the sprint(s) and whether the risk arises during development or after deployment. "Linked to" gives the IDs of the assumption (A-xx) or constraint (C-xx) in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md), or the row number in [Dependencies](03-project-canvas_v2/06-dependencies.md), that the risk comes from.

## Risk details

Copy this block for each risk.

### Template block

| Field | Content |
|---|---|
| **Risk (event)** | |
| **Linked to** | Assumption or constraint ID in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md), or row number in [Dependencies](03-project-canvas_v2/06-dependencies.md) |
| **Cause** | Why this could happen |
| **When / where** | Sprint(s); during development or after deployment |
| **Mitigation** | What is done beforehand to lower probability or impact |
| **Probability (basis)** | Residual value (1–5), plus its basis |
| **Impact (basis)** | 1–5, plus which schedule, budget or target/scope effect sets it |
| **Score** | Probability × Impact |
| **Trigger** | Numeric threshold + date or sprint |
| **Contingency plan (B plan)** | What is done if the trigger fires |
| **Owner** | Named person and the role they hold in [Project Organization](03-project-canvas_v2/08-project-organization.md) |
| **Schedule effect** | Expected delay if the contingency plan is used |

### Mitigation and basis for risks scoring below 10

| # | Mitigation | Probability basis | Impact basis |
|---|---|---|---|
| R-01 | Major Activities row 4: each text is downloaded and its article count checked in Sprint 1, before any index is built | The Law and the Regulation are published as text on mevzuat.gov.tr; the four added regulations are not yet checked | A smaller document set leaves a technical requirement (M1) partly unmet |
| R-04 | Major Activities row 12: the Law-only run goes first and its cost is checked before the larger runs | The three runs need about 20.5 million input tokens (measured token counts × 40 questions); the price of the chosen model is not yet fixed | The baseline comparison (M4) would run on fewer corpus sizes: a technical requirement is partly unmet |
| R-05 | Major Activities row 5: amendment dates checked at each sprint start; retrieval date shown with answers | The Law was amended in 2026; follow-up changes to regulations are typical after such an amendment | The document set and the answer key stay as retrieved (C-02), so answers that rest on an amended article no longer match the law in force: a technical requirement is partly unmet. The questions affected are listed as a limitation in the final report (D12); no rework |
| R-06 | Major Activities row 6: terms of use read before collecting from each source | Questions come from several sources, so losing one does not empty a question type | A secondary source is lost; under 2 weeks of extra collection |
| R-08 | Major Activities row 16: weekly spend tracking with alerts at 50% and 75% | No cost is measured yet; the long-context baseline runs alone need about 20.5 million input tokens | Running out of credit before M10 would stop the live demo, an acceptance step |
| R-09 | Major Activities row 18: work is planned per sprint and every deliverable has a second named member who can take it over | Team estimate: over 11 weeks, an absence of 2 weeks or more by one of the four members (illness, exam period) is possible but not expected | One deliverable slips by up to one sprint (2–4 weeks) |
| R-10 | Major Activities rows 10 and 17: masking before logging; logs keep anonymised data only | Masking patterns cover the formats of national ID numbers and licence plates; free-text names can be missed | A constraint (C-12) is partly unmet until the log is cleaned |
| R-12 | Major Activities row 13: results are reported by question type together with cost per question and response time, so the comparison does not rest on correctness alone | Only models with a 1-million-token window can read the full set (255,138 tokens); Li et al. (2024) report that strong long-context models can beat RAG on average, at a much higher cost; no trial run yet | A secondary metric is affected; RAG remains the solution because of C-04 |
| R-13 | Major Activities row 13: the model version is pinned in the configuration; evaluation runs are scheduled at least 3 days before each milestone | Third-party dependency; no outage observed so far | An evaluation run slips by under 2 weeks; if the model version changes between M5 and M7, the two results are not comparable (a secondary metric is affected) |
| R-14 | Major Activities row 21: the earlier turns of the session are passed to retrieval and generation | No trial run yet; a follow-up question on its own often lacks the words that identify its topic, so retrieval on the follow-up alone can miss the article | Follow-up support (C-05) is partly unmet: a technical requirement |
| R-15 | Major Activities row 28: five listed conditions, three answer strategies and at most one clarifying question, tested on the labelled question set from M5 | No trial run yet; with 8 ambiguous questions, one wrong decision moves precision or recall by about 0.12 | A wrong decision adds an unnecessary turn (Objective 1 time) or answers for the wrong condition: clarification handling (C-05) is partly unmet, a technical requirement |

Probability values without a pilot measurement are team estimates and are revised after the Sprint 1 review. No risk scores 15 or more.

### Risk R-02: too few usable questions from real sources

| Field | Content |
|---|---|
| **Risk (event)** | FAQ pages and forums yield fewer than 30 in-scope questions, or fewer than 5 in a question type, by M2 |
| **Linked to** | A-02 |
| **Cause** | Most questions on the EGM FAQ page concern procedures (queries, applications) that the six texts do not answer; forum questions often ask for an opinion on an individual case |
| **When / where** | Sprint 1; during development |
| **Mitigation** | Major Activities row 6: questions are collected from several sources and searched topic by topic (alcohol, speed, parking, inspection, driving without a licence, candidate drivers, penalty points) |
| **Probability (basis)** | 3: the first page of the EGM FAQ shows 10 questions, most of them procedural; a first forum search found 12 questions, of which about half can be answered from the six texts; 4 of the 12 were selected for question set v1 |
| **Impact (basis)** | 4: the question set is the basis of the Objective 2 success criterion |
| **Score** | 12 (High) |
| **Trigger** | On 23/10/2026 the tagged set holds fewer than 30 in-scope questions, or any question type holds fewer than 5 |
| **Contingency plan (B plan)** | The missing types are filled with team-written questions, labelled as such and limited to 10 of the 30; results are reported separately for sourced and team-written questions, and the Product Owner records the change in the charter |
| **Owner** | Ekin Deniz Öztürk, Business Analyst |
| **Schedule effect** | Under 1 week; M2 stays on 26/10/2026 |

### Risk R-03: too few test participants

| Field | Content |
|---|---|
| **Risk (event)** | Fewer than 10 participants complete the default-state session (M2) or the pilot session (M9) |
| **Linked to** | A-03; Dependencies row 3 |
| **Cause** | Participants are unpaid volunteers (classmates, colleagues and family members of the team) and the two sessions are about two months apart |
| **When / where** | Sprints 1 and 4; during development |
| **Mitigation** | Major Activities row 3: 12 people are invited so that 2 are in reserve; written confirmation by 19/10/2026 and again by M8 (14/12/2026) |
| **Probability (basis)** | 3: no written confirmation had been received on 18/10/2026 |
| **Impact (basis)** | 4: the success criteria of Objectives 1 and 3 are defined on 10 participants |
| **Score** | 12 (High) |
| **Trigger** | Fewer than 10 written confirmations on 19/10/2026, or fewer than 10 on 14/12/2026 (M8) |
| **Contingency plan (B plan)** | The test runs with the participants available (at least 6); the results of Objectives 1 and 3 are reported as counts out of the participants who took part, against the targets as written in the charter; only participants who completed both sessions are compared for Objective 1, and the Project Review Committee is informed in writing |
| **Owner** | Zehranur Aymaz Kutluyer, Product Owner |
| **Schedule effect** | None; the result is reported on fewer participants |

### Risk R-07: the assistant answers what it should decline

| Field | Content |
|---|---|
| **Risk (event)** | The assistant answers an out-of-scope question or gives advice on an individual case instead of declining |
| **Linked to** | C-01, C-05, C-11 |
| **Cause** | Language models tend to produce an answer when a retrieved article looks related; questions about contesting a penalty are close in wording to in-scope questions about the procedure |
| **When / where** | Sprints 3–4; during development and after deployment |
| **Mitigation** | Major Activities row 9: out-of-scope handling, tested on the 10 out-of-scope questions of question set v1 from the alpha onwards |
| **Probability (basis)** | 3: no trial run yet; the out-of-scope questions collected so far (insurance, individual objections) are close to in-scope topics |
| **Impact (basis)** | 4: Objective 4 requires the assistant to decline all 10 out-of-scope questions |
| **Score** | 12 (High) |
| **Trigger** | The beta answers 1 or more of the 10 out-of-scope questions in the run of 09/12/2026 |
| **Contingency plan (B plan)** | Degrade gracefully: below a retrieval-similarity threshold the assistant shows only the retrieved articles with no generated answer, and questions asking about the outcome of the user's own case receive a fixed refusal text |
| **Owner** | Barış Saka, Data Scientist |
| **Schedule effect** | About 1 week, inside Sprint 4 |

### Risk R-11: Objective 2 levels not met

| Field | Content |
|---|---|
| **Risk (event)** | The share of correct answers or of supported article references on the 30 in-scope questions is below 80% at M7 |
| **Linked to** | C-04; Objective 2 in Project Executive Summary |
| **Cause** | Retrieval misses the right article for questions in everyday language; some answers need several articles; the 2026 amendment changed provisions the language model may remember in their old form |
| **When / where** | Sprints 2–3; during development |
| **Mitigation** | Major Activities row 13: the RAG baseline is measured by question type at M5, which leaves Sprint 3 for the weakest types |
| **Probability (basis)** | 3: no trial run yet; the levels are a team estimate until M5 |
| **Impact (basis)** | 4: the 80% levels are the success criterion of Objective 2 |
| **Score** | 12 (High) |
| **Trigger** | Either share is below 70% at M5 (18/11/2026) or below 80% at M7 (09/12/2026) |
| **Contingency plan (B plan)** | Narrow the scope: generated answers are released only for the question types that reach 80%; for the other types the assistant shows the retrieved articles with no generated answer, and the Product Owner reports the Objective 2 result as measured, against the target as written in the charter, to the Project Review Committee at M8 |
| **Owner** | Zehranur Aymaz Kutluyer, Product Owner |
| **Schedule effect** | About 1 week, inside Sprint 4 |

### Example (illustrative only)

| Field | Content |
|---|---|
| **Risk (event)** | End-to-end latency does not meet the target on the available hardware |
| **Linked to** | A-04: "The allocated GPU quota supports the latency target for 20 concurrent users" |
| **Cause** | The GPU quota comes from shared cloud credits; the final allocation is not known at project start |
| **When / where** | Sprints 2-4; during development and after deployment |
| **Mitigation** | Early capacity test in Sprint 2; batching, caching and quantization trials |
| **Probability (basis)** | 3: the Sprint 2 pilot measured p95 latency at 1.6× the target |
| **Impact (basis)** | 4: latency is an acceptance criterion of the MVP deliverable |
| **Score** | 12 (High) |
| **Trigger** | p95 end-to-end latency > 2× target at the end of Sprint 4 |
| **Contingency plan (B plan)** | Switch to a smaller quantized model; renegotiate the number of concurrent users with the AI customer; move to queue-based asynchronous answers |
| **Owner** | A named team member in the Data Scientist role |
| **Schedule effect** | About 2 weeks |

## Checklist before submitting

- [ ] At least 5 risks
- [ ] At least one risk from each of the five layers (data / model / infrastructure / integration / people-process)
- [ ] Every risk is written as an event, with when and where
- [ ] Every assumption in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) has a risk here, and the IDs match both ways
- [ ] Every risk that comes from a constraint names the in-scope activity in [Major Activities](03-project-canvas_v2/04-major-activities.md) that mitigates it
- [ ] Probability values are residual (after mitigation), and each has a basis
- [ ] Risks that threaten an acceptance criterion or success criterion have an impact of at least 4
- [ ] Every risk scoring 10 or more has a mitigation, a numeric trigger with a date or sprint, a contingency plan and a named owner
- [ ] Every owner is a named person listed in [Project Organization](03-project-canvas_v2/08-project-organization.md)
- [ ] No contingency plan repeats work already planned under [Major Activities](03-project-canvas_v2/04-major-activities.md)
- [ ] Scores are spread out (not all low, not all high)
- [ ] Risk timings fall inside the project's sprint timeline
